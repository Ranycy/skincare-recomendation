<template>
  <transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[60] flex items-end justify-center bg-gray-950/45 p-0 backdrop-blur-sm sm:items-center sm:p-6">
      <div class="absolute inset-0 cursor-pointer" @click="$emit('close')"></div>

      <article class="relative max-h-[92vh] w-full overflow-hidden rounded-t-[2rem] bg-white shadow-2xl sm:max-w-4xl sm:rounded-[2rem]">
        <button
          @click="$emit('close')"
          class="absolute right-4 top-4 z-10 grid h-10 w-10 place-items-center rounded-full bg-white/90 text-gray-500 shadow-sm backdrop-blur transition hover:text-gray-900"
          aria-label="Close product detail"
        >
          <X class="h-5 w-5" />
        </button>

        <div class="max-h-[92vh] overflow-y-auto">
          <div class="grid sm:grid-cols-[0.8fr_1fr]">
            <div class="relative min-h-64 bg-gradient-to-br from-accent-pink via-white to-primary/10 p-6">
              <div class="absolute inset-0" :class="categoryWash"></div>
              <div class="relative flex h-full min-h-56 flex-col justify-between">
                <div class="flex items-start justify-between gap-3">
                  <span class="badge bg-white/80">{{ product.type }}</span>
                  <span class="rounded-full bg-primary-dark px-3 py-1 text-xs font-bold text-white">
                    #{{ product.rank }}
                  </span>
                </div>
                <div>
                  <p class="text-xs font-bold uppercase tracking-[0.16em] text-primary/75">{{ product.brand }}</p>
                  <div class="mt-4 text-8xl font-display font-bold text-primary/15">
                    {{ product.brand?.[0] || "S" }}
                  </div>
                </div>
              </div>
            </div>

            <div class="space-y-6 p-5 sm:p-8">
              <div class="space-y-3 pr-10">
                <div class="flex flex-wrap items-center gap-2">
                  <span class="badge">{{ product.matchScore }}% match</span>
                  <span class="badge bg-accent-pink/80 text-s-d">{{ product.type }}</span>
                </div>
                <h2 class="text-3xl font-bold leading-tight text-gray-950 sm:text-4xl">{{ product.name }}</h2>
                <p class="text-sm leading-6 text-gray-600">
                  Rekomendasi ini dibuat dari profil kulit, cuaca, dan preferensi kandungan yang kamu isi.
                </p>
              </div>

              <div class="grid gap-5 sm:grid-cols-2">
                <section class="space-y-3">
                  <h3 class="eyebrow">Key ingredients</h3>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="ing in product.ingredients"
                      :key="ing"
                      class="rounded-full border border-gray-100 bg-gray-50 px-3 py-1.5 text-xs font-semibold text-gray-600"
                    >
                      {{ ing }}
                    </span>
                  </div>
                </section>

                <section class="space-y-3">
                  <h3 class="eyebrow">Skin types</h3>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="skin in product.skin"
                      :key="skin"
                      class="inline-flex items-center gap-1 rounded-full bg-primary/8 px-3 py-1.5 text-xs font-bold text-primary-dark"
                    >
                      <CheckCircle2 class="h-3.5 w-3.5" />
                      {{ skin }}
                    </span>
                  </div>
                </section>
              </div>

              <section class="rounded-3xl border border-primary/10 bg-primary/5 p-5">
                <div class="mb-3 flex items-center gap-2 text-primary-dark">
                  <Info class="h-5 w-5" />
                  <h3 class="font-bold">Why this product?</h3>
                </div>
                <p class="text-sm italic leading-7 text-gray-700">
                  {{ product.whyRecommended }}
                </p>
              </section>
            </div>
          </div>
        </div>
      </article>
    </div>
  </transition>
</template>

<script setup>
import { computed } from "vue";
import { X, CheckCircle2, Info } from "lucide-vue-next";

const props = defineProps({
  product: Object,
  isOpen: Boolean,
});

const categoryWash = computed(() => {
  const type = props.product?.type || "";
  if (type.includes("sunscreen")) return "bg-[radial-gradient(circle_at_74%_18%,rgba(245,158,11,0.20),transparent_13rem)]";
  if (type.includes("cleanser")) return "bg-[radial-gradient(circle_at_74%_18%,rgba(59,130,246,0.16),transparent_13rem)]";
  if (type.includes("mask")) return "bg-[radial-gradient(circle_at_74%_18%,rgba(255,222,222,0.92),transparent_13rem)]";
  return "bg-[radial-gradient(circle_at_74%_18%,rgba(74,103,65,0.16),transparent_13rem)]";
});
</script>
