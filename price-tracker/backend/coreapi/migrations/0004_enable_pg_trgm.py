from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('coreapi', '0003_productgroup_alter_product_category_and_more'),
    ]
    
    atomic = False
    
    operations = [
        # 1. Enable extension (safe in transaction)
        migrations.RunSQL(
            sql='CREATE EXTENSION IF NOT EXISTS pg_trgm;',
            reverse_sql='DROP EXTENSION IF EXISTS pg_trgm;'
        ),

        # 2. Add GIN trigram index on canonical_name
        migrations.RunSQL(
            sql='''
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_productgroup_canonical_name_trgm
            ON coreapi_productgroup USING gin (canonical_name gin_trgm_ops);
            ''',
            reverse_sql='DROP INDEX IF EXISTS idx_productgroup_canonical_name_trgm;'
        ),
    ]