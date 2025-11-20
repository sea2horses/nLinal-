<script lang="ts">
	import { onMount } from 'svelte';

	type ThemeOption = {
		id: string;
		label: string;
		description: string;
	};

	const themeOptions: ThemeOption[] = [
		{ id: 'vscode', label: 'VS Code', description: 'Tema oscuro inspirado en VS Code.' },
		{ id: 'light', label: 'Light', description: 'Contraste suave ideal para impresiones.' },
		{ id: 'dark', label: 'Dark', description: 'Verdes profundos para sesiones largas.' },
		{ id: 'pastel', label: 'Pastel', description: 'Alta saturación tipo hacking.' },
		{ id: 'corporate', label: 'Corporate', description: 'Neutro profesional.' }
	];

	const storedTheme =
		typeof window !== 'undefined' ? window.localStorage.getItem('flyon-theme') : null;
	const storedMotion =
		typeof window !== 'undefined' ? window.localStorage.getItem('ui-motion') : null;
	const storedHints =
		typeof window !== 'undefined' ? window.localStorage.getItem('math-hints') : null;

	let currentTheme = $state(storedTheme ?? 'vscode');
	let reduceMotion = $state(storedMotion === 'off');
	let showHints = $state(storedHints !== 'off');
	let accentIntensity = $state(70);

	onMount(() => {
		applyTheme(currentTheme);
		applyMotionSetting(reduceMotion);
		applyHintSetting(showHints);
	});

	$effect(() => {
		applyTheme(currentTheme);
	});

	$effect(() => {
		applyMotionSetting(reduceMotion);
	});

	$effect(() => {
		applyHintSetting(showHints);
	});

	$effect(() => {
		if (typeof document === 'undefined') return;
		document.documentElement.style.setProperty('--accent-opacity', `${accentIntensity}%`);
	});

	function applyTheme(theme: string) {
		if (typeof document === 'undefined') return;
		document.documentElement.setAttribute('data-theme', theme);
		if (typeof window !== 'undefined') {
			window.localStorage.setItem('flyon-theme', theme);
		}
	}

	function applyMotionSetting(disableAnimations: boolean) {
		if (typeof document === 'undefined') return;
		document.documentElement.style.setProperty(
			'animation',
			disableAnimations ? 'none' : ''
		);
		if (typeof window !== 'undefined') {
			window.localStorage.setItem('ui-motion', disableAnimations ? 'off' : 'on');
		}
	}

	function applyHintSetting(enabled: boolean) {
		if (typeof window !== 'undefined') {
			window.localStorage.setItem('math-hints', enabled ? 'on' : 'off');
		}
	}
</script>

<main class="flex-1 overflow-y-auto bg-base-100 px-6 py-10 lg:px-12">
	<div class="mx-auto flex max-w-6xl flex-col gap-10">
		<header class="space-y-3">
			<p class="text-sm font-semibold uppercase tracking-wide text-primary">Configuración</p>
			<h1 class="text-4xl font-bold">Personaliza la experiencia FlyonUI</h1>
			<p class="text-sm text-base-content/70">
				Selecciona un tema, ajusta las animaciones y define preferencias para los módulos numéricos.
			</p>
		</header>

		<section class="space-y-6 rounded-2xl border border-base-300 bg-base-200/40 p-6">
			<h2 class="text-2xl font-semibold">Tema global</h2>
			<div class="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
				{#each themeOptions as option}
					<label class="card cursor-pointer rounded-2xl border border-base-300 p-4 transition hover:border-primary" data-theme={option.id}>
						<div class="flex items-center justify-between">
							<p class="text-lg font-semibold">{option.label}</p>
							<input
								type="radio"
								class="radio radio-primary"
								name="theme"
								value={option.id}
								checked={currentTheme === option.id}
								onchange={() => (currentTheme = option.id)}
							/>
						</div>
						<p class="mt-2 text-sm text-base-content/70">{option.description}</p>
						<div class="mt-3 flex gap-2">
							<span class="size-6 rounded-full bg-primary/60"></span>
							<span class="size-6 rounded-full bg-secondary/60"></span>
							<span class="size-6 rounded-full bg-accent/60"></span>
						</div>
					</label>
				{/each}
			</div>
		</section>

		<section class="grid gap-6 lg:grid-cols-2">
			<article class="rounded-2xl border border-base-300 bg-base-200/40 p-6">
				<h3 class="text-xl font-semibold">Accesibilidad</h3>
				<label class="mt-4 flex items-center justify-between gap-4">
					<div>
						<p class="font-medium">Reducir animaciones</p>
						<p class="text-sm text-base-content/70">
							Desactiva transiciones para mejorar el enfoque o ahorrar energía.
						</p>
					</div>
					<input type="checkbox" class="toggle toggle-primary" bind:checked={reduceMotion} />
				</label>
				<label class="mt-4 flex items-center justify-between gap-4">
					<div>
						<p class="font-medium">Mostrar pistas en módulos</p>
						<p class="text-sm text-base-content/70">
							Activa mensajes contextualizados para guiar al usuario en los cálculos.
						</p>
					</div>
					<input type="checkbox" class="toggle toggle-secondary" bind:checked={showHints} />
				</label>
				<label class="form-control gap-2 mt-5">
					<span class="label-text text-sm">Intensidad del acento ({accentIntensity}%)</span>
					<input
						type="range"
						min="30"
						max="100"
						step="5"
						class="range range-primary"
						bind:value={accentIntensity}
					/>
				</label>
			</article>

			<article class="rounded-2xl border border-base-300 bg-base-200/40 p-6">
				<h3 class="text-xl font-semibold">Preferencias de laboratorio</h3>
				<p class="text-sm text-base-content/70">
					Estas opciones se guardan en tu navegador y se aplican a los talleres guiados.
				</p>
				<ul class="mt-4 space-y-3 text-sm">
					<li class="flex items-center gap-3">
						<span class="badge badge-primary badge-sm">NumPy</span>
						Activar avisos de pérdida de precisión
					</li>
					<li class="flex items-center gap-3">
						<span class="badge badge-secondary badge-sm">SciPy</span>
						Mostrar recomendaciones de refinamiento
					</li>
					<li class="flex items-center gap-3">
						<span class="badge badge-accent badge-sm">Eel</span>
						Permitir llamadas al backend al abrir cada módulo
					</li>
				</ul>
				<p class="mt-4 text-xs text-base-content/60">
					Personalizar estas opciones ayuda a documentar las condiciones de simulación en tus reportes.
				</p>
			</article>
		</section>
	</div>
</main>

