<script lang="ts">
	import MathLive from './MathLive.svelte';

	interface Params {
		Header: string;
		Dimension: number;
		value: string[];
		disabled?: boolean;
	}

	let { Header, Dimension, value = $bindable<string[]>(), disabled = false }: Params = $props();
	// Keep `value` as a Columns x Headers.length 2D array.
	// Preserve existing values when possible and fill missing cells with empty strings.
	$effect(() => {
		if (!Array.isArray(value)) value = [];

		// Ensure correct number of rows
		while (value.length < Dimension) value.push('');
		if (value.length > Dimension) value.length = Dimension;
	});
</script>

<div class="max-w-full overflow-x-auto">
	<table class="table">
		<thead>
			<tr>
				<th>{Header}</th>
			</tr>
		</thead>
		<tbody>
			{#each Array(Dimension) as _, i}
				<tr>
					<td>
						<div class="cell">
							<MathLive bind:value={value[i]} {disabled} />
						</div>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	/* Fixed table layout so columns keep stable widths */
	table.table {
		table-layout: fixed;
		width: 100%;
		border-collapse: collapse;
	}

	/* Allow the inner cell to scroll horizontally without growing the column */
	td .cell {
		min-width: 0; /* allow overflow to be clipped inside cell */
		overflow: auto;
		white-space: nowrap;
	}

	/* Ensure MathLive (or its wrapper) can shrink to fit the cell */
	td .cell :global(*) {
		min-width: 0;
		max-width: 100%;
		box-sizing: border-box;
	}
</style>
