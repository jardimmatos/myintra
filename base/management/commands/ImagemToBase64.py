from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'Exemplos de Commands Django para integraçoes'

    def add_arguments(self, parser):
        parser.add_argument('--path', nargs='+', help='url da imagem')
        parser.add_argument('--type', nargs='+', help='Tupo de path')
        
   
    def handle(self, *args, **options):
        import base64
        # URL da imagem
        url = options.get('path')[0]
        
        with open(url, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode('utf-8')



