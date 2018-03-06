const spawnSync = require('child_process').spawnSync;

// 外部に関数を読み込ませる
exports.pycall_ec2_onoff = function pycall_ec2_onoff(req, res) {
  result = spawnSync('./pypy3-v5.9.0-linux64/bin/pypy3', ['./start_or_stop_ec2.py'], {
    stdio:'pipe', 
    input: JSON.stringify(req.query)
  });
  if(result.stdout){
    res.status(200).send(`<!doctype html>` + result.stdout + '\n' + result.stderr  + `</html>`);
  }else if (result.stderr){
    res.status(200).send(result.stderr)  
  }

};
