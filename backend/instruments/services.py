from io import BytesIO
import qrcode
from django.conf import settings
from django.core.files.base import ContentFile

def generate_instrument_qr(instrument):
    url = f"{settings.FRONTEND_URL.rstrip('/')}/public/verify/{instrument.uid}"
    image = qrcode.make(url)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    instrument.qr_code.save(
        f"{instrument.uid}.png",
        ContentFile(buffer.getvalue()),
        save=False,
    )
    instrument.save(update_fields=["qr_code", "updated_at"])
