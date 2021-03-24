from irctube import app


@app.cli.command()
def populate_json():
    app.logger.info('populating json...')
    # TODO: run script that populates json
    
    
    app.logger.info('successfully populated json')
