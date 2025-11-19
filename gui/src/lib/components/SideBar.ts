export type MenuItem = { name: string; href: string; icon: string };
export type Category = { name: string; items: (MenuItem | Category)[] };

export const SidebarItems: (MenuItem | Category)[] = [
    {
        name: 'Inicio',
        href: '/',
        icon: 'tabler:home'
    },
    {
        name: 'Matrices',
        items: [
            {
                name: 'Suma',
                href: '#',
                icon: 'tabler:sum'
            },
            {
                name: 'Resta',
                href: '#',
                icon: 'gg:math-minus'
            },
            {
                name: 'Multiplicación',
                href: '#',
                icon: 'mdi:multiply'
            },
            {
                name: 'Determinante',
                items: [
                    {
                        name: 'Cofactores',
                        href: '#',
                        icon: 'mdi:multiply'
                    },
                    {
                        name: 'Sarrus',
                        href: '#',
                        icon: 'mdi:multiply'
                    }
                ]
            }
        ]
    },
    {
        name: 'Vectores',
        items: [
            {
                name: 'Suma',
                href: '#',
                icon: 'tabler:sum'
            },
            {
                name: 'Resta',
                href: '#',
                icon: 'gg:math-minus'
            },
            {
                name: 'Multiplicación',
                href: '#',
                icon: 'mdi:multiply'
            },
            {
                name: 'Propiedades',
                items: [
                    {
                        name: 'Conmutativa',
                        href: '#',
                        icon: 'tabler:home'
                    }
                ]
            }
        ]
    },
    {
        name: 'Sistemas Lineales',
        items: [
            {
                name: 'Gauss-Jordan',
                href: '/gauss-jordan/',
                icon: 'tabler:function'
            },
            {
                name: 'Cramer',
                href: '#',
                icon: 'tabler:function'
            },
            {
                name: 'Combinacion Lineal',
                href: '#',
                icon: 'tabler:function'
            },
        ]
    },
    {
        name: 'Laboratorio',
        href: '#',
        icon: 'tabler:function'
    },
    {
        name: 'Configuración',
        href: '#',
        icon: 'tabler:settings'
    }
];