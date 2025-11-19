<script lang="ts">
	import Icon from '@iconify/svelte';

	import { type MenuItem, type Category } from './SideBar';
	export let Item: MenuItem | Category;
</script>

{#if 'items' in Item}
	<li>
		<p class="menu-title">{Item.name}</p>
		<ul>
			{#each Item.items as sub}
				<svelte:self Item={sub} />
			{/each}
		</ul>
	</li>
{:else}
	<li>
		<a href={Item.href} class="text-sm">
			<Icon icon={Item.icon} class="size-4" />
			{Item.name}
		</a>
	</li>
{/if}
