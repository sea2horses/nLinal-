// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
import { type MathfieldElementAttributes } from "mathlive";

declare namespace svelteHTML {
	interface IntrinsicElements {
		'math-field': MathfieldElementAttributes;
	}
}

declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}

	interface Window {
		// eel is injected at runtime by the eel package
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		eel: any | undefined;
	}

}

export { };
