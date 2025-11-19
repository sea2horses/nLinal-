const eelInstance =
    typeof window !== 'undefined' ? (window as typeof window & { eel?: typeof window.eel }).eel : undefined;

if (eelInstance) {
    eelInstance.set_host('ws://localhost:8888');
    console.log(`Eel was correctly initialized: `, eelInstance);
} else {
    console.warn(`Eel could not be initialized`);
}

export default eelInstance;

export async function callPyFunc<T>(name: string, ...args: unknown[]): Promise<T> {
    if (!eelInstance) {
        throw new Error('Eel no está disponible en esta ventana.');
    }

    const fn = eelInstance[name];

    if (!fn) {
        throw new Error(`La función "${name}" no está expuesta en Python.`);
    }

    try {
        const result: T = await fn(...args)();
        return result;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
        console.error(`Error al invocar ${name} via Eel:`, err);
        throw new Error(`No se pudo ejecutar "${name}": ${err.errorText}`);
    }
}