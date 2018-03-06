const spawnSync = require('child_process').spawnSync;

exports.pycall_ec2_shortcut = function pycall_ec2_shortcut(req, res) {
  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./ec2_shortcut.py'], {
    stdio:'pipe', 
    input: JSON.stringify(req.query)
  });
  if(result.stdout){
    res.status(200).send(`<!doctype html>` + result.stdout + '\n' + result.stderr  + `</html>`);
  }else if (result.stderr){
    res.status(200).send(result.stderr)  
  }

};
