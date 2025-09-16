import os
from dotenv import load_dotenv
import supabase
from model.Court import Court

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SupabaseClient:
    def __init__(self):
        self.client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_courts(self):
        """
        Busca todas as quadras do banco de dados.
        """
        response = self.client.table('courts').select('*').execute()
        courts = []
        for item in response.data:
            courts.append(Court(
                id=item['id'],
                name=item['name'],
                court_type=item['court_type'],
                description=item['description'],
                capacity=item['capacity'],
                price_per_hour=item['price_per_hour'],
                start_hour=item['start_hour'],
                end_hour=item['end_hour'],
            ))
        return courts

    def create_court(self, court: Court):
        """
        Cria uma quadra nova na tabela 'courts' do banco de dados, aceita um objeto Court.
        """
        court_dict = {
            "name": court.name,
            "court_type": court.court_type,
            "description": court.description,
            "capacity": court.capacity,
            "price_per_hour": court.price_per_hour,
            "start_hour": court.start_hour,
            "end_hour": court.end_hour,
        }
        response = self.client.table('courts').insert(court_dict).execute()
        return response
