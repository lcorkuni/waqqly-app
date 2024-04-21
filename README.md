## Waqqly Web App: Connecting Dog Owners and Walkers

The Waqqly Web App is a cloud-based platform that simplifies dog walking coordination. It connects dog
owners with reliable walkers, allowing them to:

* **Register and Login:** Create accounts and manage profiles.
* **Browse Dog Walkers:** Search and discover dog walkers in their area.


## Local Development

**IMPORTANT, LIKELY LIMITED FUNCTIONALITY:** Due to security measures, local development has limitations.
The database resides behind a private Azure endpoint and unless your local IP has been added to the
endpoints configuration, you will not be able to access the database. This means you will not be able
to log in, register users, or access the `/home` or `/docs`. You will be limited to accessing the
`/login` and the `/register` endpoints

**Prerequisites:**

* Python and pip installed on your system

**Running the App:**
1. **Open a shell:** e.g. Powershell or GitBash
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Environment Variables:**
   Refer to report in Appendix A to find the enviroment variables that need setting.
4. **Start the App:**
   ```bash
   python ./app.py
   ```

## Azure CI/CD Pipeline

The Waqqly Web App leverages Azure DevOps for a continuous integration
(CI/CD) pipeline. This automated process ensures efficient deployment:

* Upon a code push to Azure DevOps, a new versio of the application is automatically built.
* The built version is then deployed to the cloud environment.
