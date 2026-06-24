import httpx

from app.core.config import settings


class ArtInstituteClient:
    def __init__(self) -> None:
        self.base_url = settings.ART_INSTITUTE_API_BASE_URL

    async def get_artwork_by_id(self, external_id: int) -> dict | None:
        url = f"{self.base_url}/artworks/{external_id}"

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)

        if response.status_code in (400, 404):
            return None

        response.raise_for_status()

        data = response.json().get("data")

        if not data:
            return None

        image_id = data.get("image_id")
        image_url = None

        if image_id:
            image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"

        return {
            "external_place_id": data["id"],
            "title": data.get("title") or "Untitled",
            "artist_title": data.get("artist_title"),
            "image_url": image_url,
        }
