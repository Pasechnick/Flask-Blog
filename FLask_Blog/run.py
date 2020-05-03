from flaskblog import create_app

app = create_app() # here we can also pass a configuration as an argument, but there is already a default config included 

if __name__ == '__main__':
    app.run(debug=True)






