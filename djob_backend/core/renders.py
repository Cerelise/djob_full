from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # response = super().render(data, accepted_media_type, renderer_context)
        # response_data = self.get_response_data(response)
        # response_data['code'] = 200
        # return self.render_json(response_data)
        # print(renderer_context)
        # print(renderer_context['response'].status_code)

        if renderer_context:
            if isinstance(data,dict):
                status_code = renderer_context['response'].status_code
                code = data.pop('code',status_code)

            else:
                msg = '请求无效'
                code = 400

                # print(f'renderer:{data}')
            try:
                detail = data['detail']
                ret = {
                    'msg':detail,
                    'code':data['status_code']
                }
                return super().render(ret,accepted_media_type,renderer_context)
            except:
                msg = data['message']
                try:
                    serializer_data = data['data']
                    ret = {
                        'msg':msg,
                        'code':code,
                        'data':serializer_data,
                    }
                except:           
                    ret = {
                        'msg':msg,
                        'code':code,
                    }

                return super().render(ret,accepted_media_type,renderer_context)
        else:
            return super().render(data,accepted_media_type,renderer_context)

                #  print(json.dumps(data))
                # d = json.loads(json.dumps(data))
                # print(d)
                # print(type(d))
                # for item in d:
                #   print(item)
                #   print(type(d[item]))
                #   tmp = d[item][0].split(' ')
                #   tmp[0]  = item
                #   print(' '.join(tmp))