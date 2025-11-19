<script lang="ts">
	interface Params {
		value: number;
		min: number;
		max: number;
		label: string;
		className?: string;
		disabled?: boolean;
	}

	let {
		value = $bindable<number>(),
		min,
		max,
		label,
		className = '',
		disabled = false
	}: Params = $props();
</script>

<div class={className} data-input-number>
	<label class="label-text" for="number-input-label">{label}</label>
	<div class="input">
		<input
			type="text"
			bind:value
			aria-label="Label input number"
			data-input-number-input
			id="number-input-label"
			{disabled}
		/>
		<span class="my-auto flex gap-3">
			<button
				type="button"
				class="btn size-5.5 min-h-0 rounded-sm btn-soft p-0 btn-primary"
				aria-label="Decrement button"
				onclick={() => {
					if (value > min) value--;
				}}
				{disabled}
			>
				<span class="icon-[tabler--minus] size-3.5 shrink-0"></span>
			</button>
			<button
				type="button"
				class="btn size-5.5 min-h-0 rounded-sm btn-soft p-0 btn-primary"
				aria-label="Increment button"
				onclick={() => {
					if (value < max) value++;
				}}
				{disabled}
			>
				<span class="icon-[tabler--plus] size-3.5 shrink-0"></span>
			</button>
		</span>
	</div>
</div>
