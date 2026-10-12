import re


def extract_reference_comparisons(report_text: str) -> str:
    """Compare recognized CBC values with ranges printed in the report."""

    text = re.sub(
        r"Mean Corpuscular Hemoglobin\s+Concentration",
        "Mean Corpuscular Hemoglobin Concentration",
        report_text,
        flags=re.I,
    )
    text = re.sub(
        r"(Mean Corpuscular Hemoglobin Concentration)\s*\n\s*",
        r"\1 ", text, flags=re.I,
    )
    text = re.sub(r"\bT\s+otal\b", "Total", text, flags=re.I)

    labels = [
        "Mean Corpuscular Hemoglobin Concentration",
        "Mean Corpuscular Hemoglobin",
        "Red Blood Cell Count",
        "Total Leukocyte Count",
        "Platelet Count",
        "Mean Corpuscular Volume",
        "Hemoglobin",
        "Hematocrit",
        "Neutrophils %",
        "Lymphocytes %",
        "Monocytes %",
        "Eosinophils %",
        "Basophils %",
    ]
    labels.sort(key=len, reverse=True)

    row_pattern = re.compile(
        r"^\s*(-?\d+(?:\.\d+)?)\s+(.+?)\s+"
        r"(-?\d+(?:\.\d+)?)\s*[-–]\s*"
        r"(-?\d+(?:\.\d+)?)\s+(NORMAL|LOW|HIGH)\s*$",
        re.I,
    )

    results = []
    differential_values = {}

    for line in text.splitlines():
        line = line.strip()
        for label in labels:
            if not line.lower().startswith(label.lower()):
                continue

            remainder = line[len(label):]
            match = row_pattern.match(remainder)
            if not match:
                break

            raw_value, unit, raw_low, raw_high, lab_status = match.groups()
            value, low, high = map(
                float, (raw_value, raw_low, raw_high)
            )

            if low > high:
                break

            status = (
                "BELOW the printed range" if value < low
                else "ABOVE the printed range" if value > high
                else "WITHIN the printed range"
            )
            expected_lab_status = (
                "LOW" if value < low
                else "HIGH" if value > high
                else "NORMAL"
            )

            result = (
                f"- {label}: {value:g} {unit.strip()}; "
                f"printed range {low:g}-{high:g}; "
                f"calculated comparison: {status}."
            )

            if lab_status.upper() != expected_lab_status:
                result += (
                    f" WARNING: printed status {lab_status.upper()} "
                    "conflicts with the numeric comparison."
                )

            results.append(result)

            if label in {
                "Neutrophils %",
                "Lymphocytes %",
                "Monocytes %",
                "Eosinophils %",
                "Basophils %",
            }:
                differential_values[label] = value

            break
        required_differential_labels = {
        "Neutrophils %",
        "Lymphocytes %",
        "Monocytes %",
        "Eosinophils %",
        "Basophils %",
    }

    if required_differential_labels.issubset(differential_values):
        percentage_total = sum(differential_values.values())

        if abs(percentage_total - 100) > 2:
            results.append(
                f"- Differential percentage consistency: recognized "
                f"white-cell percentages total {percentage_total:g}%, "
                "not approximately 100%. WARNING: verify the original "
                "report; values have not been corrected."
            )


    if not results:
        return (
            "No reliable CBC range comparisons could be extracted. "
            "Do not infer or invent comparisons."
        )

    return "\n".join(results)
