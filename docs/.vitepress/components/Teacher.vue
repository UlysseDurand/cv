<script setup>
import { computed } from 'vue'

const teachers = {
    "Stéphan Thomassé": "https://perso.ens-lyon.fr/stephan.thomasse/",
    "Pascal Koiran": "https://sites.google.com/view/pascal-koiran/",
    "Daniel Hirschkoff": "https://perso.ens-lyon.fr/daniel.hirschkoff/",
    "Eddy Caron": "https://graal.ens-lyon.fr/~ecaron/Research/publications.html",
    "Anne Benoit": "https://graal.ens-lyon.fr/~abenoit/anne.benoit",
    "Natacha Portier": "https://perso.ens-lyon.fr/natacha.portier/blog/",
    "Yves Robert": "https://graal.ens-lyon.fr/~yrobert/",
    "Pierre Clairambault": "https://pageperso.lis-lab.fr/pierre.clairambault/",
    "Etienne Miquey": "https://www.i2m.univ-amu.fr/perso/etienne.miquey/",
    "Michael Rao": "https://perso.ens-lyon.fr/michael.rao/",
    "Daniel Stilck França": "https://danielstilckfranca.eu/",
    "Gabriel Radanne": "https://gabriel.radanne.net/",
    "Ludovic Henrio": "https://lhenrio.github.io/",
    "Elisa Ricietti": "https://perso.ens-lyon.fr/elisa.riccietti/",
    "Colin Riba": "https://perso.ens-lyon.fr/colin.riba/",
    "Ralph Sarkis": "https://ralphs16.github.io/",
    "Titouan Vayer": "https://tvayer.github.io/",
    "Michele Angelo Pagani": "https://perso.ens-lyon.fr/michele.pagani/",
    "Vincent Nivoliers": "https://perso.liris.cnrs.fr/vincent.nivoliers/",
    "David Coeurjolly": "https://perso.liris.cnrs.fr/david.coeurjolly/",
    "Claire Dross": "https://www.linkedin.com/in/claire-dross-6805b027/",
    "Yannick Moy": "https://www.linkedin.com/in/yannick-moy-464703/",
    "Rémi Favier": "https://www.linkedin.com/in/remi-favier-insa/",
    "Nidhi Goyal": "https://sites.google.com/a/iiitd.ac.in/nidhigoyal/",
    "Mathurin Massias": "https://mathurinm.github.io/about/",
    "Quentin Bertrand": "https://qb3.github.io",
    "Jean-Michel Muller": "https://perso.ens-lyon.fr/jean-michel.muller/",
    "Guillaume Melquiond": "https://guillaume.melquiond.fr/",
    "Claude Pierre Jeannerod": "https://perso.ens-lyon.fr/claude-pierre.jeannerod/",
    "Suraj Kumar": "https://surakuma.github.io/",
    "Loris Marchal": "https://perso.ens-lyon.fr/loris.marchal/",
    "Frédéric Vivien": "https://perso.ens-lyon.fr/frederic.vivien/",
    "Daria Pchelina": "https://perso.ens-lyon.fr/daria.pchelina/",
    "Nathalie Revol": "https://perso.ens-lyon.fr/nathalie.revol/",
    "Damien Pous": "https://perso.ens-lyon.fr/damien.pous/",
    "Edouard Bonnet": "https://perso.ens-lyon.fr/edouard.bonnet/",
    "Denis Kuperberg": "https://perso.ens-lyon.fr/denis.kuperberg/",
    "François Schwarzentruber": "https://perso.ens-lyon.fr/francois.schwarzentruber/",
    "Tanguy Risset": "http://perso.citi.insa-lyon.fr/trisset/",
    "Romain Michon": "https://ccrma.stanford.edu/~rmichon/",
    "Jean-Claude Iehl": "https://perso.univ-lyon1.fr/jean-claude.iehl/",
    "Raphaëlle Chaine": "https://perso.liris.cnrs.fr/raphaelle.chaine/",
}

const props = defineProps({
    name: {type: String, required: true},
})

const link = computed(() => teachers[props.name] || null)

</script>

<template>
    <div v-if="link">
        <a :href="link" target="_blank" rel="noopener noreferrer">{{ props.name }}</a>
    </div>
    <div v-else>
        <span>{{ props.name }}</span>
    </div>
</template>