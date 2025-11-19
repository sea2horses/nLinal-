import { callPyFunc } from '$lib/eel';

function normalizeEntry(value: string | undefined): string {
    const parsed = value;
    return parsed && parsed.length ? parsed : '0';
}

function makeAugmentedMatrix(
    coefficients: string[][],
    results: string[],
    rows: number,
    incognitas: number
): string[][] {
    const augmented: string[][] = [];

    for (let i = 0; i < rows; i++) {
        const row: string[] = [];
        for (let j = 0; j < incognitas; j++) {
            row.push(normalizeEntry(coefficients?.[i]?.[j]));
        }
        row.push(normalizeEntry(results?.[i]));
        augmented.push(row);
    }

    return augmented;
}

export async function GaussJordan(
    coefficients: string[][],
    results: string[],
    ecuaciones: number,
    incognitas: number
): Promise<string> {
    const augmented = makeAugmentedMatrix(coefficients, results, ecuaciones, incognitas);
    return callPyFunc<string>('resolver_sistema_por_gauss_jordan', augmented, ecuaciones, incognitas);
}