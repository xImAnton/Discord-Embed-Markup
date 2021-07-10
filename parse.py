import json


class NonNoneDict(dict):
	def __setitem__(self, k, v):
		if v:
			super(NonNoneDict, self).__setitem__(k, v)


class Context:
	def __init__(self):
		self.text = ""
		self.title = None
	
	def to_json(self):
		return {}


class Field(Context):
	def __init__(self):
		super(Field, self).__init__()
		self.inline = False

	def to_json(self):
		return {"name": self.title, "value": self.text, "inline": self.inline}


class Embed(Context):
	def __init__(self):
		super(Embed, self).__init__()
		self.url = None
		self.color = None
		self.timestamp = None
		self.a_name = None
		self.a_img = None
		self.a_url = None
		self.fields = []
		self.img = None
		self.thumb = None
		self.f_text = None
		self.f_img = None
		
	def cmd(self, cmd, arg):
		if cmd == "author":
			self.a_name = arg
		elif cmd == "author&":
			self.a_img = arg
		elif cmd == "url":
			self.url = arg
		elif cmd == "thumbnail":
			self.thumb = arg
		elif cmd == "footer": 
			self.f_text = arg
		elif cmd == "footer&":
			self.f_img = arg
		else:
			 return False
		return True
	
	def to_json(self):
		out = NonNoneDict({"title": self.title, "description": self.text})
		out["url"] = self.url
		out["timestamp"] = self.timestamp
		out["color"] = self.color
		if self.f_text:
			out["footer"] = NonNoneDict({"text": self.f_text})
			out["footer"]["icon_url"] = self.f_img
		out["fields"] = [f.to_json() for f in self.fields]
		if self.img:
			out["image"] = {"url": self.img}
		if self.thumb:
			out['thumbnail'] = {"url": self.thumb}
		aut = NonNoneDict()
		aut["name"] = self.a_name
		aut["url"] = self.a_url
		aut["icon_url"] = self.a_img
		out["author"] = aut
		return out


with open("test.dem") as f:
	li = f.readlines()


e = Embed()
ctx = None
prev_empty = False
for l in li:
	l = l.strip()
	if l.startswith("# "):
		e.title = l.split("# ")[1]
		ctx = e
		continue
	if l.startswith("## "):
		ctx = Field()
		ctx.title = l.split("## ")[1]
		e.fields.append(ctx)
		continue
	if l.startswith("@"):
		s = l.split(" ")
		cmd = s[0][1:]
		arg = " ".join(s[1:])
		if not e.cmd(cmd, arg):
			print("unsupported command: " + cmd)
		continue
	if l.startswith("%"):
		continue
	if l.startswith("?"):
		continue
	if prev_empty:
		l = "\n" + l
	if ctx:
		ctx.text += l
	prev_empty = bool(l.strip())

print(json.dumps({"embed": e.to_json()}, indent=2))
