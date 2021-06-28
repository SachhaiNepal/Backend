from rest_framework.exceptions import ValidationError


def validate_location(attrs):
    vdc = attrs.get("vdc")
    municipality = attrs.get("municipality")
    vdc_ward = attrs.get("vdc_ward")
    municipality_ward = attrs.get("municipality_ward")
    if (vdc and municipality) or (vdc_ward and municipality_ward):
        raise ValidationError("Both municipality and vdc fields cannot be selected.")
    elif municipality and vdc_ward:
        raise ValidationError("Cannot assign vdc ward for a municipality.")
    elif vdc and municipality_ward:
        raise ValidationError("Cannot assign municipality ward for a vdc.")
    return attrs
