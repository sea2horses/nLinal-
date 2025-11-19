<script lang="ts">
	import MathLive from './MathLive.svelte';

	interface Params {
		Headers: string[];
		Rows: number;
		value: string[][];
		disabled?: boolean;
	}

	let { Headers, Rows, value = $bindable<string[][]>(), disabled = false }: Params = $props();

	// Keep `value` as a Columns x Headers.length 2D array.
	// Preserve existing values when possible and fill missing cells with empty strings.
	$effect(() => {
		if (!Array.isArray(value)) value = [];

		// Ensure correct number of rows
		while (value.length < Rows) value.push([]);
		if (value.length > Rows) value.length = Rows;

		// Ensure each row has the correct number of columns (headers)
		const cols = Headers ? Headers.length : 0;
		for (let i = 0; i < Rows; i++) {
			if (!Array.isArray(value[i])) value[i] = [];

			while (value[i].length < cols) value[i].push('');

			if (value[i].length > cols) value[i].length = cols;
		}
	});
</script>

<div class="max-w-full overflow-x-auto">
	<table class="table">
		{#if Headers.length}
			<colgroup>
				{#each Headers as _, k}
					<col style="width: {100 / Headers.length}%" />
				{/each}
			</colgroup>
		{/if}
		<thead>
			<tr>
				{#each Headers as Header}
					<th>{Header}</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each Array(Rows) as _, i}
				<tr>
					{#each Array(Headers.length) as _, j}
						<td>
							<div class="cell">
								<MathLive bind:value={value[i][j]} {disabled} />
							</div>
						</td>
					{/each}
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
