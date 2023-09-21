const { spawn } = require('child_process');

function getPythonServiceVersion(callback) {
    const pythonProcess = spawn('python', ['agent.py']);

    pythonProcess.stdout.on('data', (data) => {
        callback(null, data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
        callback(data.toString());
    });
}

module.exports = {
    getPythonServiceVersion
};
