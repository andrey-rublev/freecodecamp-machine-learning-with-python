"""Execute portable project notebooks, retaining their real outputs and figures."""
from pathlib import Path
import base64
import contextlib
import io
import json
import os
import re
import sys
import traceback
import nbformat as nbf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

path = Path(sys.argv[1]).resolve()
os.environ.setdefault('FCC_DATA_DIR', str(path.parent / 'data'))
os.environ.setdefault('FCC_ARTIFACT_DIR', str(path.parent / 'artifacts'))
notebook = nbf.read(path, as_version=4)
namespace = {'__name__':'__main__'}
counter = 0
for index, cell in enumerate(notebook.cells):
    if cell.cell_type != 'code':
        continue
    counter += 1
    cell.execution_count = counter
    cell.outputs = []
    stream = io.StringIO()
    def show(*args, **kwargs):
        for number in plt.get_fignums():
            buffer = io.BytesIO()
            plt.figure(number).savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            cell.outputs.append(nbf.v4.new_output('display_data', data={
                'image/png':base64.b64encode(buffer.getvalue()).decode(),
                'text/plain':'<Matplotlib figure>'}))
        plt.close('all')
    plt.show = show
    print(f'Executing {path.name}, cell {index}', flush=True)
    try:
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            exec(compile(cell.source, f'{path.name}:cell{index}', 'exec'), namespace)
    except Exception as exc:
        cell.outputs.append(nbf.v4.new_output('error', ename=type(exc).__name__,
            evalue=str(exc), traceback=traceback.format_exc().splitlines()))
        nbf.write(notebook, path)
        print(stream.getvalue(), flush=True)
        raise
    text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', stream.getvalue())
    if text:
        cell.outputs.insert(0, nbf.v4.new_output('stream', name='stdout', text=text))
        print(text, end='', flush=True)
    nbf.write(notebook, path)

all_output = '\n'.join(output.get('text', '') for cell in notebook.cells
    for output in cell.get('outputs', []) if output.output_type == 'stream')
assert 'You passed the challenge' in all_output, 'Official test did not report success.'
metrics = {'notebook':path.name, 'official_test_passed':True}
for name in ['mae','percentage_identified','sms_accuracy','sms_auc']:
    if name in namespace:
        metrics[name] = float(namespace[name])
metrics_path = Path(os.environ['FCC_ARTIFACT_DIR']) / (path.stem + '_metrics.json')
metrics_path.write_text(json.dumps(metrics, indent=2))
nbf.validate(notebook)
print('VALIDATED', json.dumps(metrics), flush=True)
