import ImageUpload from "./ImageUpload";
import GoogleLogin from "react-google-login";
import { Component } from "react";

function MaybeSubmit({ image, auth, onSubmit }) {
	let disabled_message = null;

	if (!auth) {
		disabled_message = "Please authorize with Google first.";
	} else if (!image) {
		disabled_message = "Please take an image first.";
	}

	return (
		<>
			<button onClick={onSubmit} disabled={disabled_message != null}>
				Submit
			</button>
			{disabled_message && <p>{disabled_message}</p>}
		</>
	);
}

function makeMakeGoogleButton(is_authed) {
	return (renderProps) => (
		<button onClick={renderProps.onClick} disabled={renderProps.disabled}>
			Log in {is_authed ? "again " : ""}to Google
		</button>
	);
}

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			image: null,
			auth: null,
			finalUrl: null,
		};
	}
	get image() {
		return this.state.image;
	}
	set image(image) {
		this.setState({ image });
	}
	get auth() {
		return this.state.auth;
	}
	set auth(auth) {
		this.setState({ auth });
	}
	async submit() {
		console.log("Submitting!");
		let resp = await fetch("/api/submit", {
			method: "post",
			body: {
				image: this.state.image,
				auth: this.state.auth,
			},
		});
		resp = await resp.json();
		this.setState({ finalUrl: resp.url });
	}
	render() {
		if (this.state.finalUrl) {
			return <p>Your URL is <a href={this.state.finalUrl}>{this.state.finalUrl}</a>!</p>;
		}
		return (
			<>
				<GoogleLogin
					clientId="951809403294-c8ngd13qejgmlpdq05d1h6c49vjhbpr5.apps.googleusercontent.com"
					buttonText="Log in to Google"
					scope="https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/documents"
					onSuccess={(auth) => {
						this.auth = auth;
					}}
					onFailure={alert}
					render={makeMakeGoogleButton(this.state.auth != null)}
					cookiePolicy={"single_host_origin"}
				/>
				<ImageUpload
					onImage={(image) => {
						this.image = image;
					}}
				/>
				<MaybeSubmit auth={this.auth} image={this.image} onSubmit={this.submit.bind(this)} class="" />
			</>
		);
	}
}

export default App;
