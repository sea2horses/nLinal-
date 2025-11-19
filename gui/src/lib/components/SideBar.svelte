<script lang="ts">
	import Icon from '@iconify/svelte';
	import { SidebarItems } from './SideBar';
	import SideBarItem from './SideBarItem.svelte';
</script>

<div id="sidebar" class="flex h-screen flex-col justify-between border-r border-base-300">
	<div id="logo" class="flex-center gap-1 border-b border-base-300 p-3">
		<Icon icon="mdi:math-integral-box" class="size-10" />
		<p class="text-2xl font-bold">Linal</p>
	</div>
	<div id="options" class="overflow-y-auto">
		<ul class="menu overflow-x-hidden overflow-y-auto">
			{#each SidebarItems as Item}
				<SideBarItem {Item} />
			{/each}
		</ul>
	</div>
	<div class="flex h-min flex-col gap-1 border-t border-base-300 p-3">
		<p class="text-sm text-accent">Version 1.0.0</p>
		<p class="text-xs text-accent">Hecho en Python y Eel + SvelteKit</p>
	</div>
</div>
