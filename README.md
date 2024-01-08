Essential project w.r.t Data engineering: 
Converts CSV files to a json format file from a source to a target directory.\n
cmd >$Env:SRC_BASE_DIR = 'data/retail_db'; >$Env:TRG_BASE_DIR = 'data/retail_db_json'; >python app.py **or** >python app.py '[\"orders\", \"order_items\"]'
