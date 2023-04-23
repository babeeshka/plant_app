from database import db
import datetime

class Plant(db.Model):
    __tablename__ = "plants"
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(255), nullable=False)
    scientific_name = db.Column(db.String(255), nullable=False)
    sunlight_care = db.Column(db.String(255), nullable=True)
    water_care = db.Column(db.String(255), nullable=True)
    temperature_care = db.Column(db.String(255), nullable=True)
    humidity_care = db.Column(db.String(255), nullable=True)
    growing_tips = db.Column(db.String(255), nullable=True)
    propagation_tips = db.Column(db.String(255), nullable=True)
    common_pests = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    family = db.Column(db.String(255), nullable=True)
    genus = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    edible = db.Column(db.Boolean, nullable=True)
    edible_part = db.Column(db.String(255), nullable=True)
    edible_notes = db.Column(db.String(255), nullable=True)
    medicinal = db.Column(db.Boolean, nullable=True)
    medicinal_notes = db.Column(db.String(255), nullable=True)
    toxicity = db.Column(db.String(255), nullable=True)
    synonyms = db.Column(db.String(255), nullable=True)
    native_status = db.Column(db.String(255), nullable=True)
    conservation_status = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, common_name, scientific_name, sunlight_care=None, water_care=None, temperature_care=None, humidity_care=None, growing_tips=None, propagation_tips=None, common_pests=None, image_url=None, family=None, genus=None, year=None, edible=None, edible_part=None, edible_notes=None, medicinal=None, medicinal_notes=None, toxicity=None, synonyms=None, native_status=None, conservation_status=None):
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.sunlight_care = sunlight_care
        self.water_care = water_care
        self.temperature_care = temperature_care
        self.humidity_care = humidity_care
        self.growing_tips = growing_tips
        self.propagation_tips = propagation_tips
        self.common_pests = common_pests
        self.image_url = image_url
        self.family = family
        self.genus = genus
        self.year = year
        self.edible = edible
        self.edible_part = edible_part
        self.edible_notes = edible_notes
        self.medicinal = medicinal
        self.medicinal_notes = medicinal_notes
        self.toxicity = toxicity
        self.synonyms = synonyms
        self.native_status = native_status
        self.conservation_status = conservation_status

    @classmethod
    def plant_search(cls, plant_name):
        return cls.query.filter(cls.common_name.ilike(f'%{plant_name}%')).all()