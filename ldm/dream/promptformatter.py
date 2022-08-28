class PromptFormatter:
    def __init__(self, t2i=None, opt=None):
        self.t2i = t2i
        self.opt = opt

    def normalize_prompt(self):
        """Normalize the prompt and switches"""
        t2i = self.t2i
        opt = self.opt

        switches = list()
        switches.append(f'"{opt.prompt}"')
        switches.append(f'-s{opt.steps        or t2i.steps}')
        switches.append(f'-b{opt.batch_size   or t2i.batch_size}')
        switches.append(f'-W{opt.width        or t2i.width}')
        switches.append(f'-H{opt.height       or t2i.height}')
        switches.append(f'-C{opt.cfg_scale    or t2i.cfg_scale}')
        if opt.seed:
            switches.append(f'-S{opt.seed}')
        
        if opt.init_img:
            switches.append(f'-I{opt.init_img}')
        if opt.strength and opt.init_img is not None:
            switches.append(f'-f{opt.strength or t2i.strength}')
        if opt.gfpgan_strength:
            switches.append(f'-G{opt.gfpgan_strength}')
        if t2i:
            switches.append(f'-m{t2i.sampler_name}')
            if t2i.full_precision:
                switches.append('-F')
        return ' '.join(switches)