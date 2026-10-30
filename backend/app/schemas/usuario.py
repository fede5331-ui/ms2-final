from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioRegistro(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)

    @field_validator("password")
    @classmethod
    def password_hasta_72_bytes(cls, valor: str) -> str:
        if len(valor.encode("utf-8")) > 72:
            raise ValueError(
                "La contraseña no puede superar los 72 bytes "
                "(las tildes y la ñ ocupan más de un byte)"
            )
        return valor


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str