import yaml


class PluginManifestService:

    REQUIRED_FIELDS = [
        "name",
        "version",
        "entry"
    ]

    @staticmethod
    def validate(
        content: str
    ):

        try:

            data = yaml.safe_load(
                content
            )

        except Exception as e:

            return {
                "valid": False,
                "data": None,
                "errors": [
                    str(e)
                ]
            }

        errors = []

        for field in (
            PluginManifestService
            .REQUIRED_FIELDS
        ):

            if field not in data:

                errors.append(
                    f"{field} is required"
                )

        return {
            "valid":
                len(errors) == 0,

            "data":
                data,

            "errors":
                errors
        }