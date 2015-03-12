# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(default=uuid.uuid1, unique=True, max_length=255)),
                ('used', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthenticationToken',
            fields=[
                ('accesstoken_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='alumnus_backend.AccessToken')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=('alumnus_backend.accesstoken',),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('uuid', models.CharField(default=uuid.uuid1, unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('gender', models.CharField(blank=True, max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('graduation_year', models.CharField(blank=True, max_length=4, choices=[(b'1950', b'1950'), (b'1951', b'1951'), (b'1952', b'1952'), (b'1953', b'1953'), (b'1954', b'1954'), (b'1955', b'1955'), (b'1956', b'1956'), (b'1957', b'1957'), (b'1958', b'1958'), (b'1959', b'1959'), (b'1960', b'1960'), (b'1961', b'1961'), (b'1962', b'1962'), (b'1963', b'1963'), (b'1964', b'1964'), (b'1965', b'1965'), (b'1966', b'1966'), (b'1967', b'1967'), (b'1968', b'1968'), (b'1969', b'1969'), (b'1970', b'1970'), (b'1971', b'1971'), (b'1972', b'1972'), (b'1973', b'1973'), (b'1974', b'1974'), (b'1975', b'1975'), (b'1976', b'1976'), (b'1977', b'1977'), (b'1978', b'1978'), (b'1979', b'1979'), (b'1980', b'1980'), (b'1981', b'1981'), (b'1982', b'1982'), (b'1983', b'1983'), (b'1984', b'1984'), (b'1985', b'1985'), (b'1986', b'1986'), (b'1987', b'1987'), (b'1988', b'1988'), (b'1989', b'1989'), (b'1990', b'1990'), (b'1991', b'1991'), (b'1992', b'1992'), (b'1993', b'1993'), (b'1994', b'1994'), (b'1995', b'1995'), (b'1996', b'1996'), (b'1997', b'1997'), (b'1998', b'1998'), (b'1999', b'1999'), (b'2000', b'2000'), (b'2001', b'2001'), (b'2002', b'2002'), (b'2003', b'2003'), (b'2004', b'2004'), (b'2005', b'2005'), (b'2006', b'2006'), (b'2007', b'2007'), (b'2008', b'2008'), (b'2009', b'2009'), (b'2010', b'2010'), (b'2011', b'2011'), (b'2012', b'2012'), (b'2013', b'2013'), (b'2014', b'2014'), (b'2015', b'2015'), (b'2016', b'2016'), (b'2017', b'2017'), (b'2018', b'2018'), (b'2019', b'2019'), (b'2020', b'2020'), (b'2021', b'2021')])),
                ('school', models.CharField(blank=True, max_length=10, choices=[(b'CC', b'CC'), (b'SEAS', b'SEAS'), (b'GS', b'GS'), (b'BC', b'BC')])),
                ('industry', models.CharField(blank=True, max_length=100, choices=[(b'Accounting', b'Accounting'), (b'Airlines/Aviation', b'Airlines/Aviation'), (b'Alternative Dispute Resolution', b'Alternative Dispute Resolution'), (b'Alternative Medicine', b'Alternative Medicine'), (b'Animation', b'Animation'), (b'Apparel/Fashion', b'Apparel/Fashion'), (b'Architecture/Planning', b'Architecture/Planning'), (b'Arts/Crafts', b'Arts/Crafts'), (b'Automotive', b'Automotive'), (b'Aviation/Aerospace', b'Aviation/Aerospace'), (b'Banking/Mortgage', b'Banking/Mortgage'), (b'Biotechnology/Greentech', b'Biotechnology/Greentech'), (b'Broadcast Media', b'Broadcast Media'), (b'Building Materials', b'Building Materials'), (b'Business Supplies/Equipment', b'Business Supplies/Equipment'), (b'Capital Markets/Hedge Fund/Private Equity', b'Capital Markets/Hedge Fund/Private Equity'), (b'Chemicals', b'Chemicals'), (b'Civic/Social Organization', b'Civic/Social Organization'), (b'Civil Engineering', b'Civil Engineering'), (b'Commercial Real Estate', b'Commercial Real Estate'), (b'Computer Games', b'Computer Games'), (b'Computer Hardware', b'Computer Hardware'), (b'Computer Networking', b'Computer Networking'), (b'Computer Software/Engineering', b'Computer Software/Engineering'), (b'Computer/Network Security', b'Computer/Network Security'), (b'Construction', b'Construction'), (b'Consumer Electronics', b'Consumer Electronics'), (b'Consumer Goods', b'Consumer Goods'), (b'Consumer Services', b'Consumer Services'), (b'Cosmetics', b'Cosmetics'), (b'Dairy', b'Dairy'), (b'Defense/Space', b'Defense/Space'), (b'Design', b'Design'), (b'E-Learning', b'E-Learning'), (b'Education Management', b'Education Management'), (b'Electrical/Electronic Manufacturing', b'Electrical/Electronic Manufacturing'), (b'Entertainment/Movie Production', b'Entertainment/Movie Production'), (b'Environmental Services', b'Environmental Services'), (b'Events Services', b'Events Services'), (b'Executive Office', b'Executive Office'), (b'Facilities Services', b'Facilities Services'), (b'Farming', b'Farming'), (b'Financial Services', b'Financial Services'), (b'Fine Art', b'Fine Art'), (b'Fishery', b'Fishery'), (b'Food Production', b'Food Production'), (b'Food/Beverages', b'Food/Beverages'), (b'Fundraising', b'Fundraising'), (b'Furniture', b'Furniture'), (b'Gambling/Casinos', b'Gambling/Casinos'), (b'Glass/Ceramics/Concrete', b'Glass/Ceramics/Concrete'), (b'Government Administration', b'Government Administration'), (b'Government Relations', b'Government Relations'), (b'Graphic Design/Web Design', b'Graphic Design/Web Design'), (b'Health/Fitness', b'Health/Fitness'), (b'Higher Education/Acadamia', b'Higher Education/Acadamia'), (b'Hospital/Health Care', b'Hospital/Health Care'), (b'Hospitality', b'Hospitality'), (b'Human Resources/HR', b'Human Resources/HR'), (b'Import/Export', b'Import/Export'), (b'Individual/Family Services', b'Individual/Family Services'), (b'Industrial Automation', b'Industrial Automation'), (b'Information Services', b'Information Services'), (b'Information Technology/IT', b'Information Technology/IT'), (b'Insurance', b'Insurance'), (b'International Affairs', b'International Affairs'), (b'International Trade/Development', b'International Trade/Development'), (b'Internet', b'Internet'), (b'Investment Banking/Venture', b'Investment Banking/Venture'), (b'Investment Management', b'Investment Management'), (b'Judiciary', b'Judiciary'), (b'Law Enforcement', b'Law Enforcement'), (b'Law Practice/Law Firms', b'Law Practice/Law Firms'), (b'Legal Services', b'Legal Services'), (b'Legislative Office', b'Legislative Office'), (b'Leisure/Travel', b'Leisure/Travel'), (b'Library', b'Library'), (b'Logistics/Procurement', b'Logistics/Procurement'), (b'Luxury Goods/Jewelry', b'Luxury Goods/Jewelry'), (b'Machinery', b'Machinery'), (b'Management Consulting', b'Management Consulting'), (b'Maritime', b'Maritime'), (b'Market Research', b'Market Research'), (b'Marketing/Advertising/Sales', b'Marketing/Advertising/Sales'), (b'Mechanical or Industrial Engineering', b'Mechanical or Industrial Engineering'), (b'Media Production', b'Media Production'), (b'Medical Equipment', b'Medical Equipment'), (b'Medical Practice', b'Medical Practice'), (b'Mental Health Care', b'Mental Health Care'), (b'Military Industry', b'Military Industry'), (b'Mining/Metals', b'Mining/Metals'), (b'Motion Pictures/Film', b'Motion Pictures/Film'), (b'Museums/Institutions', b'Museums/Institutions'), (b'Music', b'Music'), (b'Nanotechnology', b'Nanotechnology'), (b'Newspapers/Journalism', b'Newspapers/Journalism'), (b'Non-Profit/Volunteering', b'Non-Profit/Volunteering'), (b'Oil/Energy/Solar/Greentech', b'Oil/Energy/Solar/Greentech'), (b'Online Publishing', b'Online Publishing'), (b'Other Industry', b'Other Industry'), (b'Outsourcing/Offshoring', b'Outsourcing/Offshoring'), (b'Package/Freight Delivery', b'Package/Freight Delivery'), (b'Packaging/Containers', b'Packaging/Containers'), (b'Paper/Forest Products', b'Paper/Forest Products'), (b'Performing Arts', b'Performing Arts'), (b'Pharmaceuticals', b'Pharmaceuticals'), (b'Philanthropy', b'Philanthropy'), (b'Photography', b'Photography'), (b'Plastics', b'Plastics'), (b'Political Organization', b'Political Organization'), (b'Primary/Secondary Education', b'Primary/Secondary Education'), (b'Printing', b'Printing'), (b'Professional Training', b'Professional Training'), (b'Program Development', b'Program Development'), (b'Public Relations/PR', b'Public Relations/PR'), (b'Public Safety', b'Public Safety'), (b'Publishing Industry', b'Publishing Industry'), (b'Railroad Manufacture', b'Railroad Manufacture'), (b'Ranching', b'Ranching'), (b'Real Estate/Mortgage', b'Real Estate/Mortgage'), (b'Recreational Facilities/Services', b'Recreational Facilities/Services'), (b'Religious Institutions', b'Religious Institutions'), (b'Renewables/Environment', b'Renewables/Environment'), (b'Research Industry', b'Research Industry'), (b'Restaurants', b'Restaurants'), (b'Retail Industry', b'Retail Industry'), (b'Security/Investigations', b'Security/Investigations'), (b'Semiconductors', b'Semiconductors'), (b'Shipbuilding', b'Shipbuilding'), (b'Sporting Goods', b'Sporting Goods'), (b'Sports', b'Sports'), (b'Staffing/Recruiting', b'Staffing/Recruiting'), (b'Supermarkets', b'Supermarkets'), (b'Telecommunications', b'Telecommunications'), (b'Textiles', b'Textiles'), (b'Think Tanks', b'Think Tanks'), (b'Tobacco', b'Tobacco'), (b'Translation/Localization', b'Translation/Localization'), (b'Transportation', b'Transportation'), (b'Utilities', b'Utilities'), (b'Venture Capital/VC', b'Venture Capital/VC'), (b'Veterinary', b'Veterinary'), (b'Warehousing', b'Warehousing'), (b'Wholesale', b'Wholesale'), (b'Wine/Spirits', b'Wine/Spirits'), (b'Wireless', b'Wireless'), (b'Writing/Editing', b'Writing/Editing')])),
                ('company', models.CharField(max_length=100, blank=True)),
                ('current_state', models.CharField(blank=True, max_length=50, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('times_requested', models.IntegerField(default=0)),
                ('times_completed', models.IntegerField(default=0)),
                ('last_requested', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('uuid', models.CharField(default=uuid.uuid1, unique=True, max_length=100)),
                ('members', models.ManyToManyField(to='alumnus_backend.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('uuid', models.CharField(default=uuid.uuid1, unique=True, max_length=100)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='memberlist',
            name='organization',
            field=models.ForeignKey(to='alumnus_backend.Organization'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='organization',
            field=models.ForeignKey(to='alumnus_backend.Organization'),
            preserve_default=True,
        ),
    ]
