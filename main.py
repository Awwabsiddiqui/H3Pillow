from PIL import Image , ImageOps
import os
import time
import boto3
from flask import *


app = Flask(__name__)

@app.route('/')
def upload():
    return render_template("file_upload_form.html")

@app.route('/success', methods=['POST'])
def success():
        if request.method == 'POST':
            img = request.files['file']
            img.save(img.filename)


        t = str(time.time())

        dim1 = (192, 192)
        dim2 = (512, 512)
        dim3 = (1024, 1024)

        for f in os.listdir('.'):
            if f.endswith('.jpg') or f.endswith('.png') or f.endswith('jpeg'):
                img = Image.open(f)
                fn, fext = os.path.splitext(f)
                ow, oh = img.size
                if ow > oh:
                    oh, ow = img.size
                else:
                    oh, ow = img.size

                fn, fext = os.path.splitext(f)

                img.thumbnail(dim1)
                nw, nh = img.size
                wb = int((dim1[0] - nw) / 2)
                hb = int((dim1[1] - nh) / 2)
                img = ImageOps.expand(img, border=(wb, hb), fill='white')
                img.save('output/{}_{}_{}x{}_{}'.format(fn,t, dim1[0], dim1[1], fext))

                img = Image.open(f)
                img.thumbnail(dim2)
                nw, nh = img.size
                wb = int((dim2[0] - nw) / 2)
                hb = int((dim2[1] - nh) / 2)
                img = ImageOps.expand(img, border=(wb, hb), fill='white')
                img.save('output/{}_{}_{}x{}_{}'.format(fn,t, dim2[0], dim2[1], fext))

                img = Image.open(f)
                img.thumbnail(dim3)
                nw, nh = img.size
                wb = int((dim3[0] - nw) / 2)
                hb = int((dim3[1] - nh) / 2)
                img = ImageOps.expand(img, border=(wb, hb), fill='white')
                img.save('output/{}_{}_{}x{}_{}'.format(fn,t ,dim3[0], dim3[1], fext))

                # AWS : 124798121196
                '''
                s3 = boto3.resource('s3')
                s3.meta.client.upload_file('output/{}_{}_{}x{}_{}'.format(fn,t ,dim1[0], dim1[1], fext) , 'h3-assets' , str('{}_{}_{}x{}_{}'.format(fn,t ,dim1[0], dim1[1], fext)))
                s3.meta.client.upload_file('output/{}_{}_{}x{}_{}'.format(fn,t ,dim2[0], dim2[1], fext), 'h3-assets' , str('{}_{}_{}x{}_{}'.format(fn,t ,dim2[0], dim2[1], fext)))
                s3.meta.client.upload_file('output/{}_{}_{}x{}_{}'.format(fn,t ,dim3[0], dim3[1], fext) , 'h3-assets' , str('{}_{}_{}x{}_{}'.format(fn,t ,dim3[0], dim3[1], fext)))

                os.remove(str(fn+fext))
                os.remove(str('output/{}_{}_{}x{}_{}'.format(fn,t ,dim1[0], dim1[1], fext)))
                os.remove(str('output/{}_{}_{}x{}_{}'.format(fn,t ,dim2[0], dim2[1], fext)))
                os.remove(str('output/{}_{}_{}x{}_{}'.format(fn,t ,dim3[0], dim3[1], fext)))
                '''

                r1 = str('https://testresize2.s3.us-east-2.amazonaws.com/'+str('{}_{}_{}x{}_{}'.format(fn,t ,dim1[0], dim1[1], fext)))
                r2 = str('https://testresize2.s3.us-east-2.amazonaws.com/'+str('{}_{}_{}x{}_{}'.format(fn,t ,dim2[0], dim2[1], fext)))
                r3 = str('https://testresize2.s3.us-east-2.amazonaws.com/'+str('{}_{}_{}x{}_{}'.format(fn,t ,dim3[0], dim3[1], fext)))

                return {"Small": r1, "Medium": r2, "Large": r3}


if __name__ == '__main__':
    app.run(debug=True)