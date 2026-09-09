from collections import defaultdict
import re
import pandas as pd

def generate_lset_script(REPORT_FILE, OUTPUT_MOS_FILE):
    """
    REPORT_FILE      -> Comparison Excel file path
    OUTPUT_MOS_FILE  -> Output .mos file path

    Returns generated mos file path.
    """

    # Remove these lines
    # REPORT_FILE = "Ericsson_Comparison_Report.xlsx"
    # OUTPUT_MOS_FILE = "Fix_Mismatches_GPL_Script.mos"

    ###########################################################
    # Paste your remaining code here
    ###########################################################


    RIM_REF_MAP = {
        "A": "GNBDUFunction=1,RimRSGlobal=1,RimRSSet=7",
        "B": "GNBDUFunction=1,RimRSGlobal=1,RimRSSet=8",
        "C": "GNBDUFunction=1,RimRSGlobal=1,RimRSSet=9",
    }

    TARGET_RIM_PARAMS = {"rimaggressorrssetref", "rimvictimrssetref"}

    # Explicit mapping to ensure 1/0 values are preserved exactly as in logs
    BOOL_TO_NUM_MAP = {
        "true": "1",
        "false": "0",
    }


    def get_static_rim_ref(dn: str, param: str) -> str:
        """Returns the hardcoded static reference string if parameter matches

        RIM reference rules and DN matches cell pattern A, B, or C.
        """
        if param.lower() in TARGET_RIM_PARAMS:
            match = re.search(r"NRCellDU=[^,]*?([ABC])(?:,|$)", dn)
            if match:
                cell_letter = match.group(1)
                return RIM_REF_MAP.get(cell_letter, "")
        return ""


    def get_eutran_upper_layer_ind(dn: str, param: str) -> str:
        """Handles cell-specific logic for primaryUpperLayerInd in EUtranCellFDD.

        - If 'F8' or 'F5' is found after 'EUtranCellFDD=' -> "0"
        - Otherwise for EUtranCellFDD -> "1"
        """
        if param.lower() == "primaryupperlayerind":
            # Check if DN contains EUtranCellFDD instance
            match = re.search(r"EUtranCellFDD=([^,]+)", dn, re.IGNORECASE)
            if match:
                cell_value = match.group(1).strip().upper()
                if "F8" in cell_value or "F5" in cell_value:
                    return "0"
                return "1"
        return ""


    def clean_and_preserve_value(val_raw: str, param_name: str = "") -> str:
        """Cleans raw string values, preserves numeric representations for booleans,

        and formats startTime / stopTime values strictly to HH:MM.
        """
        cleaned = re.sub(r"\s*\(.*?\)", "", str(val_raw)).strip()

        val_lower = cleaned.lower()
        if val_lower in BOOL_TO_NUM_MAP:
            return BOOL_TO_NUM_MAP[val_lower]

        # Handle startTime / stopTime HH:MM truncation
        param_lower = param_name.lower()
        if "starttime" in param_lower or "stoptime" in param_lower:
            # Match HH:MM pattern (e.g. extracts '20:30' from '20:30:00' or ISO time strings)
            time_match = re.search(r"\b([0-1]?[0-9]|2[0-3]):([0-5][0-9])\b", cleaned)
            if time_match:
                hh, mm = time_match.group(1), time_match.group(2)
                return f"{int(hh):02d}:{mm}"

        return cleaned



    try:
        REPORT_FILE.seek(0)
        xls = pd.ExcelFile(REPORT_FILE)
    except Exception as e:
        raise Exception(f"Error opening file: {e}")

    lset_commands = []
    total_mismatches = 0

    # Dictionary to aggregate all struct sub-parameters (e.g., csiRsConfig4P, csiRsConfig32P, csiRsConfig8P)
    # Structure: {(clean_dn, parent_struct): {sub_param: clean_val, ...}}
    struct_map = defaultdict(dict)
    command_sequence = []

    # Process MO_Comparison and Feature_Comparison sheets
    for sheet_name in ["MO_Comparison", "Feature_Comparison"]:
        if sheet_name not in xls.sheet_names:
            continue

        df = pd.read_excel(
            xls, sheet_name=sheet_name, dtype=str, keep_default_na=False
        )

        if "Result" not in df.columns:
            continue

        target_results = ["MISMATCH from GPL", "MISSING from Configuration"]
        filtered_df = df[df["Result"].isin(target_results)]

        for _, row in filtered_df.iterrows():
            dn_raw = row.get("DN", "")
            param_raw = row.get("Parameter/Key", "")
            result_status = row.get("Result", "").strip()

            param = str(param_raw).strip()
            clean_param = re.sub(r"\[\d+\]", "", param)

            # --- SPECIAL HANDLING FOR FEATURE_COMPARISON SHEET ---
            if sheet_name == "Feature_Comparison":
                gpl_val_raw = str(row.get("GPL Value", "")).strip()
                if not gpl_val_raw:
                    gpl_val_raw = str(row.get("FINAL GPL(UPDATED)", "")).strip()

                clean_val = clean_and_preserve_value(gpl_val_raw, clean_param)

                if result_status == "MISMATCH from GPL":
                    feature_key = (
                        clean_param if clean_param else str(dn_raw).strip()
                    )

                    if (
                        feature_key
                        and clean_val
                        and clean_val.lower() not in ["nan", "none"]
                    ):
                        cmd = f"lset {feature_key} featureState {clean_val}"
                        command_sequence.append(("SINGLE", cmd))
                        total_mismatches += 1
                elif result_status == "MISSING from Configuration":
                    dn = str(dn_raw).strip()
                    clean_dn = re.sub(
                        r"^.*?\bManagedElement=[^,]+,\s*",
                        "",
                        dn,
                        flags=re.IGNORECASE,
                    )
                    if clean_dn:
                        cmd = f"create {clean_dn}"
                        command_sequence.append(("SINGLE", cmd))
                        total_mismatches += 1

                continue

            # --- STANDARD HANDLING FOR MO_COMPARISON SHEET ---
            if not str(dn_raw).strip():
                continue

            dn = str(dn_raw).strip()

            # --- CELL/MO OVERRIDE CHECKS ---
            static_rim_val = get_static_rim_ref(dn, clean_param)
            eutran_upper_layer_val = get_eutran_upper_layer_ind(dn, clean_param)

            if static_rim_val:
                clean_val = static_rim_val
            elif eutran_upper_layer_val != "":
                clean_val = eutran_upper_layer_val
            else:
                # Priority given to "FINAL GPL(UPDATED)" with fallback to "GPL Value"
                gpl_val_raw = str(row.get("FINAL GPL(UPDATED)", "")).strip()
                if not gpl_val_raw:
                    gpl_val_raw = str(row.get("GPL Value", "")).strip()

                clean_val = clean_and_preserve_value(gpl_val_raw, clean_param)

            # Clean DN by stripping ManagedElement prefix
            clean_dn = re.sub(
                r"^.*?\bManagedElement=[^,]+,\s*", "", dn, flags=re.IGNORECASE
            )

            # Case 1: Missing MO Creation
            if result_status == "MISSING from Configuration" and (
                not clean_param or clean_param.lower() in ["nan", "none", "mo"]
            ):
                command_sequence.append(("SINGLE", f"create {clean_dn}"))
                total_mismatches += 1

            # Case 2: Struct / Nested parameters with dot notation (e.g., csiRsConfig4P.csiRsControl4Ports)
            elif "." in clean_param:
                if not clean_val or clean_val.lower() in ["nan", "none"]:
                    continue

                parent_struct, sub_param = clean_param.split(".", 1)

                key = (clean_dn, parent_struct)
                # Register unique struct instance in execution sequence
                if key not in struct_map:
                    command_sequence.append(("STRUCT", key))

                # Collect all sub-parameters under this struct (e.g., csiRsConfig4P)
                struct_map[key][sub_param] = clean_val

            # Case 3: Standard MO parameter setting
            else:
                if not clean_val or clean_val.lower() in ["nan", "none"]:
                    continue
                command_sequence.append(
                    ("SINGLE", f"lset {clean_dn} {clean_param} {clean_val}")
                )
                total_mismatches += 1

    # Format aggregated struct commands and single commands
    for item_type, data in command_sequence:
        if item_type == "SINGLE":
            lset_commands.append(data)
        elif item_type == "STRUCT":
            clean_dn, parent_struct = data
            sub_params = struct_map[data]

            # Construct comma-separated key=value assignments (e.g., sub1=val1,sub2=val2,sub3=val3)
            kv_pairs = ",".join(
                [f"{sub_k}={sub_v}" for sub_k, sub_v in sub_params.items()]
            )
            cmd = f"set {clean_dn} {parent_struct} {kv_pairs}"
            lset_commands.append(cmd)
            total_mismatches += 1

    # Write generated commands to MOS script file
    with open(OUTPUT_MOS_FILE, "w", encoding="utf-8") as f:
        f.write(
            "// =========================================================\n"
        )
        f.write(
            "// ERICSSON MISMATCH & MISSING MO SCRIPT USING GPL VALUES\n"
        )
        f.write(f"// Generated from: {REPORT_FILE.name}\n")
        f.write(f"// Total commands: {total_mismatches}\n")
        f.write(
            "// =========================================================\n\n"
        )

        for command in lset_commands:
            f.write(f"{command}\n")

    return OUTPUT_MOS_FILE
