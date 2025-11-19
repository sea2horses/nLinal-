<script lang="ts">
	import MatrixInput from '$lib/components/MatrixInput.svelte';
	import NumberInput from '$lib/components/NumberInput.svelte';
	import VectorInput from '$lib/components/VectorInput.svelte';
	import Katex from '$lib/components/Katex.svelte';
	import Icon from '@iconify/svelte';

	import { GaussJordan } from '$lib/services/gauss_jordan';

	let rows: number = $state(3);
	let columns: number = $state(3);
	let headers: string[] = $state([]);
	let matrix: string[][] = $state([]);
	let results: string[] = $state([]);

	let loading: boolean = $state(false);
	let latexOutput: string | null = $state(null);
	let errorMessage: string | null = $state(null);

	$effect(() => {
		headers.length = columns;
		for (let i = 0; i < columns; i++) {
			headers[i] = `x${i + 1}`;
		}
	});

	const hasEnoughData = () => {
		if (!rows || !columns) return false;
		const filledRows = matrix
			.slice(0, rows)
			.every((row) => row?.some((cell) => Boolean(cell?.trim())));
		const filledResults = results.slice(0, rows).every((cell) => Boolean(cell?.trim()));
		return filledRows && filledResults;
	};

	const onSolve = async () => {
		console.log($state.snapshot(matrix));

		if (loading) return;

		if (!hasEnoughData()) {
			errorMessage = 'Completa al menos una fila y todos los resultados antes de resolver.';
			return;
		}

		loading = true;
		errorMessage = null;

		try {
			const res = await GaussJordan(matrix, results, rows, columns);
			latexOutput = res;
		} catch (err) {
			errorMessage =
				err instanceof Error ? err.message : 'No se pudo resolver el sistema. Intenta de nuevo.';
			latexOutput = null;
		} finally {
			loading = false;
		}
	};

	const canDisableSolve = $derived(loading || !rows || !columns);
</script>

<main class="flex min-h-screen w-full flex-col items-center gap-6 px-4 py-8">
	<section class="text-center">
		<p class="text-sm font-semibold text-primary uppercase">Método Gauss-Jordan</p>
		<h1 class="text-4xl font-bold">Resuelve sistemas paso a paso</h1>
		<p class="text-base text-base-content/80">
			Introduce la matriz de coeficientes y el vector de resultados. El backend en Python te
			mostrará los pasos en LaTeX.
		</p>
	</section>

	<section
		class="grid w-full max-w-6xl items-start gap-6 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,0.7fr)]"
	>
		<div class="card-border card flex flex-col gap-6 rounded-2xl p-6 lg:min-w-[360px]">
			<header class="flex flex-col gap-2">
				<h2 class="text-xl font-semibold">Configura tu sistema</h2>
				<p class="text-sm text-base-content/70">
					Admite números enteros, decimales y fracciones (ej. 3/4).
				</p>
			</header>

			<div class="grid gap-3 sm:grid-cols-2">
				<NumberInput
					bind:value={rows}
					min={1}
					max={6}
					label="Filas (ecuaciones)"
					disabled={loading}
				/>
				<NumberInput
					bind:value={columns}
					min={1}
					max={6}
					label="Columnas (incógnitas)"
					disabled={loading}
				/>
			</div>

			<div class="grid gap-5 lg:grid-cols-[3fr_1fr]">
				<div class="card-border card rounded-2xl p-4">
					<p class="mb-3 text-sm font-semibold text-base-content/70">Coeficientes</p>
					<MatrixInput Headers={headers} Rows={rows} bind:value={matrix} disabled={loading} />
				</div>

				<div class="card-border card rounded-2xl p-4">
					<p class="mb-3 text-sm font-semibold text-base-content/70">Resultados</p>
					<VectorInput Header="R" Dimension={rows} bind:value={results} disabled={loading} />
				</div>
			</div>

			<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
				<p class="text-sm text-base-content/70">
					Tip: deja en blanco cualquier celda vacía y se asumirá como 0.
				</p>

				<button
					class="btn min-w-36 justify-center btn-primary"
					type="button"
					onclick={onSolve}
					disabled={canDisableSolve}
				>
					{#if loading}
						<Icon icon="line-md:loading-loop" class="size-4.5" />
					{/if}
					Resolver
				</button>
			</div>
		</div>

		<div class="card-border card flex min-h-[320px] min-w-0 flex-col gap-4 rounded-2xl p-6">
			<header class="space-y-1">
				<h2 class="text-xl font-semibold">Salida en LaTeX</h2>
				<p class="text-sm text-base-content/70">
					Visualiza los pasos o copia el código para tu informe.
				</p>
			</header>

			{#if loading}
				<div
					class="flex flex-1 flex-col items-center justify-center gap-2 text-sm text-base-content/70"
				>
					<Icon icon="line-md:loading-loop" class="size-8" />
					Procesando sistema...
				</div>
			{:else if errorMessage}
				<div class="alert text-sm alert-error">{errorMessage}</div>
			{:else if latexOutput}
				<div
					class="prose max-h-[420px] min-w-0 overflow-auto rounded-xl bg-base-200/60 p-4 text-center"
				>
					<Katex math={latexOutput} displayMode />
				</div>
				<details class="w-full">
					<summary class="cursor-pointer text-sm font-semibold text-primary"
						>Ver LaTeX crudo</summary
					>
					<textarea
						class="textarea-bordered textarea mt-2 h-32 w-full text-xs"
						readonly
						value={latexOutput}
					></textarea>
				</details>
			{:else}
				<p class="text-sm text-base-content/70">
					Ingresa tu sistema y pulsa "Resolver" para ver los pasos de Gauss-Jordan aquí mismo.
				</p>
			{/if}
		</div>
	</section>
</main>
