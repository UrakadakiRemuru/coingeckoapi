from core.utilities import CoinData
from core.utilities.exceptions import ValidationError
from core.validator import AbstractValidator


class CoinValidator(AbstractValidator):
    def __init__(self, obj: CoinData, many: bool = False):
        super().__init__(obj, many)

    def validate(self) -> CoinData | list[CoinData]:
        if self.many:
            result: list[CoinData] = []
            for obj in self.obj:
                result.append(self.validate_fields(obj))
        else:
            result: CoinData = self.validate_fields(self.obj)
        return result

    def validate_fields(self, obj: CoinData):
        result: CoinData = {}
        for field_name, field_value in obj.items():
            result[field_name] = getattr(self, f'validate_{field_name}')(field_value)
        return result

    def validate_name(self, value: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f'Coin name must be a string, but got {value} with type {type(value)}.')
        return value

    def validate_total_volume(self, value: int) -> int:
        if not isinstance(value, int):
            raise ValidationError(f'Total volume must be a number, but got {value} with type {type(value)}.')
        return value

    def validate_networks(self, value: list[str | None]) -> list[str | None]:
        if not isinstance(value, list):
            raise ValidationError(f'Networks must be a list, but got {value} with type {type(value)}.')
        if value:
            return value
        raise ValidationError(f'Networks is empty.')

    def validate_exchanges(self, value: list[str]) -> list[str]:
        if not isinstance(value, list):
            raise ValidationError(f'Exchanges must be a list, but got {value} with type {type(value)}.')
        return value

    def validate_genesis_date(self, value: str) -> str:
        if not isinstance(value, str):
            raise ValidationError(f'Genesis date must be a str, but got {value} with type {type(value)}.')
        return value
