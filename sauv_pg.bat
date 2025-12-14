@echo off
D:\postgresql-18.1-1-windows-x64-binaries\pgsql\bin\pg_dump ^
  --dbname=postgresql://alt:alt@127.0.0.1:5432/adl ^
  -w ^
  --format=tar ^
  --blobs ^
  --verbose ^
  --schema=w_sadr_artaux ^
  --file="D:\Downloads\adl_w_sadr_artaux.tar"
pause
