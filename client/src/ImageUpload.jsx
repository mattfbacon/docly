import { Component } from "react";
import Webcam from "react-webcam";

class ImageUpload extends Component {
	constructor(props) {
		super(props);
		this.onImage = props.onImage;
		this.state = {
			taking: false,
			image: null,
		};
	}
	render() {
		if (this.state.taking) {
			return (
				<Webcam>
					{({ getScreenshot }) => (
						<button
							onClick={() => {
								const image = getScreenshot();
								this.setState({ image, taking: false });
								this.onImage(image);
							}}
						>
							Capture photo
						</button>
					)}
				</Webcam>
			);
		} else {
			return <>
				{this.state.image && <img src={this.state.image} alt="Your captured image" />}
				<button onClick={() => this.setState({ taking: true })}>{this.state.image ? "Replace" : "Take"} image</button>
			</>;
		}
	}
}

export default ImageUpload;
