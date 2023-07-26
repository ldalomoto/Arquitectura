/*################################################################################################*/
/*####################################### CLIENTE MQTT ###########################################*/
/*################################################################################################*/

//var wsbroker = "192.168.0.3";  //mqtt websocket enabled broker
//var wsbroker = "localhost";
var wsbroker = "broker.hivemq.com";

//var wsport = 8083 // port for above
var wsport = 1883; // port for above

var client = new Paho.MQTT.Client(
	wsbroker,
	Number(8000),
	"myclientid_" + parseInt(Math.random() * 100, 10)
);

client.onConnectionLost = function (responseObject) {
	console.log("connection lost: " + responseObject.errorMessage);
};

/*################################################################################################*/
/*####################################### LLEGA EL MENSAJE########################################*/
/*################################################################################################*/

client.onMessageArrived = function (message) {
	let destination = message.destinationName;
	if (destination === "merequetengue") {
		let response = JSON.parse(message.payloadString);
		dataFormat = response;
		let dataCPU = dataFormat.CPU;
		let dataMemory = dataFormat.Memory;
		let dataDisco = dataFormat.Disco;
        
		//console.log(dataFormat);
		//console.log(parseFloat(dataFormat.value));
		//Crear datos CPU, Memoria y Almacenamiento 

		addData(
			myChart,
			parseFloat(dataCPU),
			
		);

		addData_Memory(
			Grafica2,
			parseFloat(dataMemory),
			
		);
		

		addData_Disco(
			Grafica3,
			parseFloat(dataDisco),
			
		);
	}
};

var options = {
	timeout: 3,
	onSuccess: function () {
		console.log("mqtt connected");
		// Connection succeeded; subscribe to our topic, you can add multile lines of these
		client.subscribe("merequetengue", { qos: 1 });
	},
	onFailure: function (message) {
		console.log("Connection failed: " + message.errorMessage);
	},
};

function init() {
	client.connect(options);
}
