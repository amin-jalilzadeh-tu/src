def run_analysis():
    pc6_input = request.args.get('pc6')
    print(f"Received pc6 input: {pc6_input}")  
    conn_params = get_conn_params()  
    print(f"Database connection parameters: {conn_params}")
    output_dir = get_idf_config()['output_dir']
    print(f"Output directory: {output_dir}")  # Debug: Check output directory config

    
    table_name = "test_pc6"

    try:


        ### Temporal fix
        buildings_df = fetch_buildings_data(table_name, conn_params)
        print(f"Fetched Data: {buildings_df.head()}")

        ###

        update_idf_and_save(buildings_df, output_dir) # df, 
        print(f"Updated IDF and saved.")
        simulate_all()  # This could also generate additional data if necessary
        print(f"Simulation completed.")
        #filename = generate_excel(pc6_input)
        #print(f"Sending file: {filename}")
        #return send_file(filename, as_attachment=True, download_name=f'{pc6_input}_results.xlsx')

    except Exception as e:
        return jsonify({"error": str(e)}), 500