from rest_framework import serializers


def validate_location(serializer_data):
    municipality = serializer_data.get("municipality")
    vdc = serializer_data.get("vdc")
    municipality_ward = serializer_data.get("municipality_ward")
    vdc_ward = serializer_data.get("vdc_ward")

    if not municipality and not vdc:
        raise serializers.ValidationError(
            "One of the municipality or vdc must be assigned."
        )
    if municipality and vdc:
        raise serializers.ValidationError(
            "Both municipality and vdc cannot be assigned."
        )
    if not municipality_ward and not vdc_ward:
        raise serializers.ValidationError(
            "One of the municipality or vdc ward must be assigned."
        )
    if municipality_ward and vdc_ward:
        raise serializers.ValidationError(
            "Both municipality or vdc ward cannot be assigned."
        )
    if municipality and vdc_ward:
        raise serializers.ValidationError(
            "Municipality and vdc ward is not an expected location combination."
        )
    if vdc and municipality_ward:
        raise serializers.ValidationError(
            "Vdc and municipality ward is not an expected location combination."
        )
    return serializer_data
