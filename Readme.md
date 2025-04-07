
✔ Your Prisma schema was created at prisma/schema.prisma
  You can now open it in your favorite editor.
  You can now open it in your favorite editor.
  You can now open it in your favorite editor.

Next steps:
1. Set the DATABASE_URL in the .env file to point to your existing database. If your database has no tables yet, read https://pris.ly/d/getting-started     
2. Set the provider of the datasource block in schema.prisma to match your database: postgresql, mysql, sqlite, sqlserver, mongodb or cockroachdb.
3. Run prisma db pull to turn your database schema into a Prisma schema.
4. Run prisma generate to generate the Prisma Client. You can then start querying your database.
5. Tip: Explore how you can extend the ORM with scalable connection pooling, global caching, and real-time database events. Read: https://pris.ly/cli/beyond-orm

More information in our documentation:
https://pris.ly/d/getting-started


**Recreate the Environment on Another Machine**

- python -m venv .venv
# open src then run source active to activate Venv
- source venv/Scripts/activate  # On Windows
- pip install -r requirements.txt

run python main:
uvicorn main:app --host 0.0.0.0 --port 5000 --reload

run typescript:
npm run dev 
