<script lang="ts">
	import 'mathlive/fonts.css';
	import 'mathlive';
	import type { MathfieldElement, MathfieldElementAttributes } from 'mathlive';
	import { on } from 'svelte/events';

	type Props = { value?: string; disabled?: boolean } & Partial<MathfieldElementAttributes>;

	let { value = $bindable(), disabled = false, ...rest }: Props = $props();

	const init = (node: MathfieldElement) => {
		$effect(() => {
			if (value) node.value = value;
		});
		$effect(() => {
			return on(node, 'input', () => {
				value = node.value;
			});
		});
	};
</script>

<math-field use:init {...rest} class="block w-full text-2xl" {disabled}></math-field>

<style>
	math-field::part(menu-toggle) {
		display: none;
	}
</style>
