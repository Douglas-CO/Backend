from rest_framework import serializers
from usuarios.models.theme_models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['uuid', 'name', 'code', 'description',
                  'palette', 'state', 'created_at', 'modified_at']

    def validate_palette(self, value):
        required_keys = ['primary', 'secondary_first',
                         'secondary_second', 'secondary_third']
        for key in required_keys:
            if key not in value:
                raise serializers.ValidationError(
                    f"El palette debe incluir la clave '{key}'")
        return value
