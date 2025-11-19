<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import SideBar from '$lib/components/SideBar.svelte';
	import eel from '$lib/eel';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<main class="flex h-screen w-screen">
	<SideBar />
	{@render children()}
</main>
