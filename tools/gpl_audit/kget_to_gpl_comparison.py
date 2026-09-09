import os
import re
import pandas as pd
from collections import defaultdict

# all your existing imports
# import re
# from collections import defaultdict
# ...

def compare_kget_gpl(GPL_FILE, LOG_FILE, OUTPUT):
    """
    GPL_FILE -> path of uploaded GPL excel
    LOG_FILE -> path of uploaded log
    OUTPUT   -> output excel path

    Returns output path.
    """

    #############################################################
    # Paste your COMPLETE existing code here
    #############################################################

    #############################################################
    # VALUE NORMALIZATION & REF STRIPPING
    #############################################################


    def normalize_ref_value(val_str):
        """Strips node-level prefix authorities like 'ManagedElement=XXXXX'

        and standardizes reference paths so they are compared purely
        by their relative MO structure.
        """
        if not val_str or pd.isna(val_str):
            return ""

        val_str = str(val_str).strip()

        # Strip ManagedElement and leading/trailing separators
        cleaned = re.sub(
            r"ManagedElement=[^,/]+", "", val_str, flags=re.IGNORECASE
        )
        cleaned = re.sub(r"^[,/ ]+", "", cleaned)
        cleaned = re.sub(r"[,/ ]+$", "", cleaned)

        # Split into RDN components and rebuild clean relative path
        parts = [p.strip() for p in re.split(r"[,/]", cleaned) if p.strip()]
        return ",".join(parts).lower()


    def clean_param_key(k):
        """Normalizes parameter keys to ensure array indices like [1] match exactly.

        Removes accidental whitespace before the bracket and lowercases. Example:
        'arpPrioEm5qi5List [1]' -> 'arpprioem5qi5list[1]'
        """
        return re.sub(r"\s+\[", "[", str(k)).strip().lower()


    def normalize_value(value):
        if pd.isna(value):
            return ""

        # Intercept boolean objects explicitly before string transformation
        if isinstance(value, bool):
            return "1" if value else "0"

        if isinstance(value, float) and value.is_integer():
            value = int(value)

        value = str(value).strip().lower()

        if "(" in value:
            value = value.split("(")[0].strip()

        if value.endswith(".0"):
            value = value[:-2]

        # Explicit text-to-bit mapping layout translation rules
        mapping = {
            "true": "1",
            "false": "0",
            "enabled": "1",
            "disabled": "0",
            "yes": "1",
            "no": "0",
            "activated": "1",
            "deactivated": "0",
        }

        return mapping.get(value, value)


    def clean_mo_class_string(mo_str):
        """Standardizes complex multi-tier class paths containing '=' signs

        into a lowercase, space-stripped format for reliable indexing.
        """
        if not mo_str or pd.isna(mo_str):
            return ""
        cleaned = re.sub(r"\s*([,=])\s*", r"\1", str(mo_str).strip())
        return cleaned.lower()


    def is_value_match(gpl_val, kget_val):
        """Evaluates direct equality first, then falls back to normalized reference matching."""
        norm_gpl = normalize_value(gpl_val)
        norm_kget = normalize_value(kget_val)

        # Direct normalized string/numeric match
        if norm_gpl == norm_kget:
            return True

        # Relative reference structural match (e.g. EUtranFrequencyRef, etc.)
        ref_gpl = normalize_ref_value(gpl_val)
        ref_kget = normalize_ref_value(kget_val)

        if ref_gpl and ref_kget and (ref_gpl == ref_kget):
            return True

        return False


    #############################################################
    # READ GPL BASELINE (Identical Column Formats)
    #############################################################

    try:
        GPL_FILE.seek(0)
        gpl_mo = pd.read_excel(GPL_FILE, sheet_name="MO")
        gpl_mo.columns = gpl_mo.columns.str.strip()
    except Exception as e:
        gpl_mo = None
        print(f"MO sheet not loaded or missing: {e}")

    try:
        GPL_FILE.seek(0)
        gpl_feature = pd.read_excel(GPL_FILE, sheet_name="Feature")
        gpl_feature.columns = gpl_feature.columns.str.strip()
    except Exception as e:
        gpl_feature = None
        print(f"Feature sheet not loaded or missing: {e}")

    #############################################################
    # PARSE KGET LOG FILE (Proxy Id & MO Boundaries)
    #############################################################

    try:
        # with open(LOG_FILE, encoding="utf-8", errors="ignore") as f:
        #     text = f.read()
        LOG_FILE.seek(0)
        text = LOG_FILE.read().decode("utf-8", errors="ignore")
    except Exception as e:
        text = ""
        print(f"Could not read log file: {e}")

    text = text.replace("\r\n", "\n")

    # Check if the log file contains LTE cells (EUtranCell variants)
    has_lte_cells = bool(re.search(r"eutrancell", text, re.IGNORECASE))
    if not has_lte_cells:
        print(
            "Optimization Notice: No LTE cells (EUtranCell) detected in log file."
            " 'ENodeBFunction' targets will be excluded from comparison."
        )

    proxy_blocks = re.split(r"={20,}\nProxy Id\s+\d+", text)

    # List to hold every individual MO instance block found in the log
    parsed_instances = []
    feature_map = {}

    for block in proxy_blocks:
        mo_match = re.search(r"MO\s+(.+)", block)
        if not mo_match:
            continue

        dn = mo_match.group(1).strip()
        dn_clean = clean_mo_class_string(dn)
        mo_name = dn.split(",")[-1]
        mo_class = mo_name.split("=")[0].strip()
        mo_class_lower = mo_class.lower()

        # Skip processing if we don't have LTE cells and this block is part of ENodeBFunction
        if not has_lte_cells and mo_class_lower == "enodebfunction":
            continue

        block_data = defaultdict(dict)
        current_mo_scope = mo_class_lower

        for line in block.splitlines():
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # RULE 1: Detect Struct boundary and set sub-scope context
            if "struct" in line_stripped.lower():
                struct_match = re.search(
                    r"\bStruct\b\s+([A-Za-z0-9_]+)", line_stripped, re.IGNORECASE
                )
                if struct_match:
                    current_mo_scope = struct_match.group(1).strip().lower()
                    continue

            # RULE 2: Detect '>>>' parameters within Struct, parse key/value split by '='
            if line_stripped.startswith(">>>"):
                clean_sub_hdr = line_stripped.replace(">>>", "").strip()

                if "=" in clean_sub_hdr:
                    parts = clean_sub_hdr.split("=", 1)
                    sub_param_raw = parts[0].strip()
                    sub_param_val = parts[1].strip()

                    # Strip leading numeric array indexing if present (e.g. "1.filterTime" -> "filterTime")
                    if "." in sub_param_raw and re.match(
                        r"^\d+\.", sub_param_raw
                    ):
                        sub_param_raw = sub_param_raw.split(".", 1)[1].strip()

                    clean_sub_key = clean_param_key(sub_param_raw)

                    # Store parameter under active struct scope
                    block_data[current_mo_scope][clean_sub_key] = {
                        "original_key": sub_param_raw,
                        "value": sub_param_val,
                    }

                    # Also expose via composite dot-notation under root MO class (e.g. structName.param)
                    composite_key = f"{current_mo_scope}.{clean_sub_key}"
                    block_data[mo_class_lower][composite_key] = {
                        "original_key": f"{current_mo_scope}.{sub_param_raw}",
                        "value": sub_param_val,
                    }
                continue

            # RULE 3: Regular parameter line -> automatically resets scope back to parent MO
            m = re.match(r"^([^\s\[]+(?:\s*\[\d+\])?)\s+(.*)", line_stripped)
            if m:
                key = m.group(1).strip()
                value = m.group(2).strip()

                if key == "MO":
                    continue

                current_mo_scope = mo_class_lower
                key_clean = clean_param_key(key)

                block_data[mo_class_lower][key_clean] = {
                    "original_key": key,
                    "value": value,
                }

        # Store every isolated scope layer inside this instance explicitly
        for class_scope, params in block_data.items():
            if not has_lte_cells and class_scope == "enodebfunction":
                continue

            parsed_instances.append({
                "dn": dn,
                "dn_clean": dn_clean,
                "mo_class_orig": (
                    mo_class if class_scope == mo_class_lower else class_scope
                ),
                "mo_class_root": mo_class_lower,
                "target_scope_lower": class_scope,
                "params": params,
            })

        # Track featureState variables linked to CXC Feature keys
        if mo_class_lower in block_data:
            primary_params = block_data[mo_class_lower]
            cxc_match = re.search(r"(CXC\d+)", dn, re.IGNORECASE) or re.search(
                r"(CXC\d+)", block, re.IGNORECASE
            )
            if cxc_match:
                cxc_id = cxc_match.group(1).upper()
                state_val = (
                    primary_params.get("featurestate", {}).get("value")
                    or primary_params.get("activated", {}).get("value")
                    or primary_params.get("state", {}).get("value")
                    or "unknown"
                )
                feature_map[cxc_id] = {
                    "dn": dn,
                    "mo_class": mo_class,
                    "value": state_val,
                }

    results_mo = []
    results_feature = []

    # ###########################################################
    # COMPARE SHEET: MO (Iterate every instance & compare every time)
    # ###########################################################
    if gpl_mo is not None and not gpl_mo.empty:
        excel_mo_map = defaultdict(lambda: defaultdict(list))

        for _, row in gpl_mo.iterrows():
            target = str(row.get("Parent MO Class", "")).strip()
            parameter = str(row.get("Parameter", "")).strip()
            gpl_value = row.get("FINAL GPL (UPDATED)", "")

            if (
                not target
                or target in ("nan", "None")
                or not parameter
                or parameter in ("nan", "None")
            ):
                continue

            target_key = clean_mo_class_string(target)

            # Skip registering baseline expectations for ENodeBFunction if LTE cells are missing
            if not has_lte_cells and target_key == "enodebfunction":
                continue

            param_clean = clean_param_key(parameter)

            excel_mo_map[target_key][param_clean].append({
                "orig_target": target,
                "orig_param": parameter,
                "gpl_value": gpl_value,
            })

        matched_excel_rules = set()

        for obj in parsed_instances:
            dn = obj["dn"]
            dn_clean = obj["dn_clean"]
            mo_class_orig = obj["mo_class_orig"]
            mo_class_root = obj["mo_class_root"]
            target_scope_lower = obj["target_scope_lower"]
            log_params = obj["params"]

            processed_log_keys = set()

            # Phase 1: Direct Matching (Includes dynamic dot notation processing)
            for param_clean_key, p_info in log_params.items():
                kget_value = p_info["value"]
                orig_param_name = p_info["original_key"]
                lookup_key = param_clean_key

                # Structs / Dot-notation parameter handling
                matched_via_dot_notation = False

                if (
                    target_scope_lower != mo_class_root
                    and mo_class_root in excel_mo_map
                ):
                    composite_dot_key = f"{target_scope_lower}.{lookup_key}"
                    if composite_dot_key in excel_mo_map[mo_class_root]:
                        processed_log_keys.add(param_clean_key)
                        matched_via_dot_notation = True
                        for ex_item in excel_mo_map[mo_class_root][
                            composite_dot_key
                        ]:
                            matched_excel_rules.add((
                                mo_class_root,
                                composite_dot_key,
                            ))
                            status = (
                                "MATCH with GPL"
                                if is_value_match(
                                    ex_item["gpl_value"], kget_value
                                )
                                else "MISMATCH from GPL"
                            )

                            results_mo.append({
                                "MO/Feature": ex_item["orig_target"],
                                "DN": dn,
                                "Parameter/Key": ex_item["orig_param"],
                                "GPL Value": str(ex_item["gpl_value"]),
                                "KGET Value": str(kget_value),
                                "Result": status,
                            })

                if matched_via_dot_notation:
                    continue

                # Standard Audit Check Logic
                excel_params = excel_mo_map.get(target_scope_lower, {})
                matched_target_key = (
                    target_scope_lower if target_scope_lower in excel_mo_map else None
                )

                if not excel_params and target_scope_lower == mo_class_orig.lower():
                    matched_key = next(
                        (k for k in excel_mo_map if dn_clean.endswith(k)), None
                    )
                    if matched_key:
                        excel_params = excel_mo_map[matched_key]
                        matched_target_key = matched_key

                current_excel_lookup = excel_params
                current_matched_target = matched_target_key

                # Fall back to checking root parent parameters if missing from structured layer map
                if (
                    lookup_key not in current_excel_lookup
                    and mo_class_root in excel_mo_map
                ):
                    if lookup_key in excel_mo_map[mo_class_root]:
                        current_excel_lookup = excel_mo_map[mo_class_root]
                        current_matched_target = mo_class_root

                if lookup_key in current_excel_lookup:
                    processed_log_keys.add(param_clean_key)
                    for ex_item in current_excel_lookup[lookup_key]:
                        if current_matched_target:
                            matched_excel_rules.add((
                                current_matched_target,
                                lookup_key,
                            ))

                        status = (
                            "MATCH with GPL"
                            if is_value_match(ex_item["gpl_value"], kget_value)
                            else "MISMATCH from GPL"
                        )

                        results_mo.append({
                            "MO/Feature": ex_item["orig_target"],
                            "DN": dn,
                            "Parameter/Key": ex_item["orig_param"],
                            "GPL Value": str(ex_item["gpl_value"]),
                            "KGET Value": str(kget_value),
                            "Result": status,
                        })

                # Audit Check B: Dot-notation sub-parameter lookup fallback handling
                else:
                    dot_matches = [
                        ex_k
                        for ex_k in current_excel_lookup
                        if "." in ex_k and ex_k.split(".", 1)[1] == lookup_key
                    ]
                    if dot_matches:
                        processed_log_keys.add(param_clean_key)
                        for matched_dot_key in dot_matches:
                            parent_prefix = matched_dot_key.split(".", 1)[0]
                            if (
                                parent_prefix == target_scope_lower
                                or target_scope_lower == mo_class_orig.lower()
                            ):
                                if current_matched_target:
                                    matched_excel_rules.add((
                                        current_matched_target,
                                        matched_dot_key,
                                    ))
                                for ex_item in current_excel_lookup[
                                    matched_dot_key
                                ]:
                                    status = (
                                        "MATCH with GPL"
                                        if is_value_match(
                                            ex_item["gpl_value"], kget_value
                                        )
                                        else "MISMATCH from GPL"
                                    )

                                    results_mo.append({
                                        "MO/Feature": ex_item["orig_target"],
                                        "DN": dn,
                                        "Parameter/Key": ex_item["orig_param"],
                                        "GPL Value": str(ex_item["gpl_value"]),
                                        "KGET Value": str(kget_value),
                                        "Result": status,
                                    })

            # Phase 2: Log entries fully missing from the GPL Excel definitions
            for param_clean_key, p_info in log_params.items():
                if param_clean_key not in processed_log_keys:
                    if (
                        mo_class_root in excel_mo_map
                        and param_clean_key in excel_mo_map[mo_class_root]
                    ):
                        continue
                    if (
                        mo_class_root in excel_mo_map
                        and f"{target_scope_lower}.{param_clean_key}"
                        in excel_mo_map[mo_class_root]
                    ):
                        continue
                    results_mo.append({
                        "MO/Feature": mo_class_orig,
                        "DN": dn,
                        "Parameter/Key": p_info["original_key"],
                        "GPL Value": "",
                        "KGET Value": str(p_info["value"]),
                        "Result": "Not part of GPL",
                    })

        # Loop through baseline parameters to explicitly catch anything "MISSING" from the log file
        for target_key, excel_params in excel_mo_map.items():
            for param_clean_key, items in excel_params.items():
                if (target_key, param_clean_key) not in matched_excel_rules:
                    for item in items:
                        results_mo.append({
                            "MO/Feature": item["orig_target"],
                            "DN": "",
                            "Parameter/Key": item["orig_param"],
                            "GPL Value": str(item["gpl_value"]),
                            "KGET Value": "",
                            "Result": "MISSING from Configuration",
                        })

    # ###########################################################
    # COMPARE SHEET: FEATURE (Auditing Mapped featureState Parameters)
    # ###########################################################
    if gpl_feature is not None and not gpl_feature.empty:
        processed_features = set()

        for _, row in gpl_feature.iterrows():
            target = str(row.get("Parent MO Class", "")).strip()
            parameter = str(row.get("Parameter", "")).strip().upper()
            gpl_value = row.get("FINAL GPL (UPDATED)", "")

            if not parameter or parameter in ("NAN", "NONE"):
                continue

            if (
                not has_lte_cells
                and clean_mo_class_string(target) == "enodebfunction"
            ):
                continue

            processed_features.add(parameter)

            if parameter in feature_map:
                match_info = feature_map[parameter]
                kget_value = match_info["value"]
                dn = match_info["dn"]
                mo_class = match_info["mo_class"]

                status = (
                    "MATCH with GPL"
                    if is_value_match(gpl_value, kget_value)
                    else "MISMATCH from GPL"
                )

                results_feature.append({
                    "MO/Feature": (
                        target
                        if target not in ("", "nan", "None")
                        else f"Feature ({mo_class})"
                    ),
                    "DN": dn,
                    "Parameter/Key": parameter,
                    "GPL Value": str(gpl_value),
                    "KGET Value": str(kget_value),
                    "Result": status,
                })
            else:
                results_feature.append({
                    "MO/Feature": (
                        target
                        if target not in ("", "nan", "None")
                        else "Feature"
                    ),
                    "DN": "",
                    "Parameter/Key": parameter,
                    "GPL Value": str(gpl_value),
                    "KGET Value": "",
                    "Result": "MISSING from Configuration",
                })

        for log_cxc, log_feat_info in feature_map.items():
            if log_cxc not in processed_features:
                if (
                    not has_lte_cells
                    and log_feat_info["mo_class"].lower() == "enodebfunction"
                ):
                    continue
                results_feature.append({
                    "MO/Feature": f"Feature ({log_feat_info['mo_class']})",
                    "DN": log_feat_info["dn"],
                    "Parameter/Key": log_cxc,
                    "GPL Value": "",
                    "KGET Value": str(log_feat_info["value"]),
                    "Result": "Not part of GPL",
                })

    #############################################################
    # SAVE & EXPORT WORKBOOK
    #############################################################

    df_mo = pd.DataFrame(results_mo)
    df_feat = pd.DataFrame(results_feature)
    df_all = pd.concat([df_mo, df_feat], ignore_index=True)

    if not df_all.empty:
        summary = (
            df_all["Result"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Count")
        )
    else:
        summary = pd.DataFrame(columns=["Status", "Count"])

    with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
        if not df_mo.empty:
            df_mo.to_excel(writer, sheet_name="MO_Comparison", index=False)
        if not df_feat.empty:
            df_feat.to_excel(writer, sheet_name="Feature_Comparison", index=False)
        if not summary.empty:
            summary.to_excel(writer, sheet_name="Summary", index=False)

    print(f"Done Processing. Total parsed audit entries generated: {len(df_all)}")

    #############################################################

    # At end of your code

    return OUTPUT