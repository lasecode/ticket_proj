"""
Seed the database with demo events and user accounts.

Run with:  python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time, timedelta
from events.models import Event
from bookings.models import Booking

User = get_user_model()

EVENTS = [
    {
        'title': 'Lagos Tech Conference 2026',
        'description': (
            'Join the biggest technology conference in West Africa! '
            'Featuring keynotes from top engineers, workshops on AI, cloud computing, '
            'and Web3, plus networking sessions with 2,000+ tech professionals.'
        ),
        'location': 'Eko Convention Centre, Lagos',
        'date': date.today() + timedelta(days=15),
        'time': time(9, 0),
        'category': Event.Category.TECHNOLOGY,
        'price': 5000,
        'total_tickets': 500,
        'is_featured': True,
    },
    {
        'title': 'Afrobeats Music Festival',
        'description': (
            'Experience the best of Afrobeats, Afropop, and Highlife music in one incredible night. '
            'Featuring Burna Boy, Wizkid, Davido and many more artists on multiple stages. '
            'Food vendors, art installations, and after-party access included.'
        ),
        'location': 'Tafawa Balewa Square, Lagos',
        'date': date.today() + timedelta(days=22),
        'time': time(18, 0),
        'category': Event.Category.CONCERT,
        'price': 15000,
        'total_tickets': 2000,
        'is_featured': True,
    },
    {
        'title': 'Startup Founders Summit',
        'description': (
            'A one-day intensive summit for entrepreneurs and startup founders. '
            'Learn from seasoned investors, hear from successful founders, and pitch '
            'your idea in front of a live panel. Includes access to post-event investor meetups.'
        ),
        'location': 'Oriental Hotel, Lagos',
        'date': date.today() + timedelta(days=30),
        'time': time(8, 30),
        'category': Event.Category.BUSINESS,
        'price': 8500,
        'total_tickets': 300,
        'is_featured': False,
    },
    {
        'title': 'Nigerian Premier League Finals Night',
        'description': (
            'Watch the thrilling finals of the Nigerian Premier League live at the stadium! '
            'Experience the electrifying atmosphere as the top two teams battle for the championship title. '
            'Refreshments, fan zones, and celebrity appearances.'
        ),
        'location': 'National Stadium, Abuja',
        'date': date.today() + timedelta(days=10),
        'time': time(16, 0),
        'category': Event.Category.SPORTS,
        'price': 3500,
        'total_tickets': 10000,
        'is_featured': True,
    },
    {
        'title': 'Digital Marketing Masterclass',
        'description': (
            'A hands-on one-day masterclass covering SEO, social media advertising, content strategy, '
            'and email marketing. Perfect for business owners, marketers, and students. '
            'Certificate of completion provided.'
        ),
        'location': 'Business Hub, Port Harcourt',
        'date': date.today() + timedelta(days=18),
        'time': time(10, 0),
        'category': Event.Category.EDUCATION,
        'price': 2000,
        'total_tickets': 100,
        'is_featured': False,
    },
    {
        'title': 'Nollywood Awards Night 2026',
        'description': (
            'The glitz and glamour of Nollywood in one spectacular evening! '
            'Watch your favourite actors and directors collect their awards. '
            'Red carpet, live performances, and an after-party you cannot miss.'
        ),
        'location': 'Eko Hotel, Lagos',
        'date': date.today() + timedelta(days=40),
        'time': time(19, 0),
        'category': Event.Category.ENTERTAINMENT,
        'price': 12000,
        'total_tickets': 800,
        'is_featured': True,
    },
    {
        'title': 'Python & Django Workshop',
        'description': (
            'A beginner-friendly two-day coding workshop. Learn Python basics, build a Django REST API, '
            'and deploy your first web application. Laptops required. All skill levels welcome.'
        ),
        'location': 'Co-Creation Hub, Lagos',
        'date': date.today() + timedelta(days=25),
        'time': time(9, 0),
        'category': Event.Category.TECHNOLOGY,
        'price': 1500,
        'total_tickets': 50,
        'is_featured': False,
    },
    {
        'title': 'Abuja International Trade Fair',
        'description': (
            'Connect with over 500 exhibitors from across Africa and beyond. '
            'Explore opportunities in manufacturing, agriculture, technology, and services. '
            'Free entry for registered businesses; general admission tickets available.'
        ),
        'location': 'International Conference Centre, Abuja',
        'date': date.today() + timedelta(days=35),
        'time': time(8, 0),
        'category': Event.Category.BUSINESS,
        'price': 500,
        'total_tickets': 5000,
        'is_featured': False,
    },
    {
        'title': 'Kano Marathon 2026',
        'description': (
            'Run through the historic streets of Kano in this annual marathon event. '
            'Categories: full marathon (42km), half marathon (21km), and 10km fun run. '
            'Medals, prizes, and post-race refreshments for all finishers.'
        ),
        'location': 'Emir\'s Palace, Kano',
        'date': date.today() + timedelta(days=45),
        'time': time(6, 30),
        'category': Event.Category.SPORTS,
        'price': 1000,
        'total_tickets': 3000,
        'is_featured': False,
    },
    {
        'title': 'Women in Leadership Forum',
        'description': (
            'An empowering one-day forum celebrating women in business, politics, and tech. '
            'Panel discussions, mentorship sessions, and a closing networking dinner. '
            'Open to all genders who support women\'s empowerment.'
        ),
        'location': 'Sheraton Hotel, Abuja',
        'date': date.today() + timedelta(days=20),
        'time': time(9, 30),
        'category': Event.Category.EDUCATION,
        'price': 3000,
        'total_tickets': 250,
        'is_featured': False,
    },
    {
        'title': 'Comedy Night with Basketmouth',
        'description': (
            'An evening of non-stop laughter with Nigeria\'s top comedians. '
            'Hosted by Basketmouth with special appearances from AY, Bovi, and more. '
            'Dinner show — table bookings available. 18+ only.'
        ),
        'location': 'MUSON Centre, Lagos',
        'date': date.today() + timedelta(days=12),
        'time': time(20, 0),
        'category': Event.Category.ENTERTAINMENT,
        'price': 7500,
        'total_tickets': 400,
        'is_featured': True,
    },
    {
        'title': 'Cybersecurity Bootcamp',
        'description': (
            'A three-day intensive bootcamp covering ethical hacking, penetration testing, '
            'and network security fundamentals. Hands-on labs, real-world scenarios, '
            'and industry certification prep included.'
        ),
        'location': 'Andela Campus, Lagos',
        'date': date.today() + timedelta(days=50),
        'time': time(9, 0),
        'category': Event.Category.TECHNOLOGY,
        'price': 10000,
        'total_tickets': 80,
        'is_featured': False,
    },
]


class Command(BaseCommand):
    help = 'Populates the database with demo events and user accounts.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing events and bookings before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Booking.objects.all().delete()
            Event.objects.all().delete()
            User.objects.filter(is_superuser=False).exclude(email='admin@example.com').delete()
            self.stdout.write(self.style.WARNING('Cleared existing data.'))

        # Create demo accounts
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created or not admin.has_usable_password():
            admin.set_password('Admin123!')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  Created admin@example.com'))
        else:
            self.stdout.write('  admin@example.com already exists - skipped.')

        regular_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Demo',
                'last_name': 'User',
                'is_staff': False,
            },
        )
        if created or not regular_user.has_usable_password():
            regular_user.set_password('User123!')
            regular_user.save()
            self.stdout.write(self.style.SUCCESS('  Created user@example.com'))
        else:
            self.stdout.write('  user@example.com already exists - skipped.')

        # Create demo events
        self.stdout.write('\nSeeding events...')
        created_count = 0
        for data in EVENTS:
            event, created = Event.objects.get_or_create(
                title=data['title'],
                defaults={**data, 'available_tickets': data['total_tickets']},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {event.title}'))
            else:
                self.stdout.write(f'  Exists:  {event.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n[OK] Done! {created_count} event(s) created.\n'
                f'\nDemo credentials:\n'
                f'  Admin:   admin@example.com / Admin123!\n'
                f'  User:    user@example.com  / User123!\n'
            )
        )
