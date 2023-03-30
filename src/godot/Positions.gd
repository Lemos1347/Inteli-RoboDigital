extends OptionButton

func _ready():
	$HTTPRequest.connect("request_completed", self, "_on_request_completed")
	$HTTPRequest.request("http://127.0.0.1:3001/all")

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse(body.get_string_from_utf8()).result
		for position in json:
			if not str(position.id) in self.items:
				self.add_item(str(position.id))

func _on_Positions_pressed():
	$HTTPRequest.request("http://127.0.0.1:3001/all")
