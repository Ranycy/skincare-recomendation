<template>
  <article class="card group flex h-full cursor-pointer flex-col" @click="$emit('view-details', product)">
    <div class="relative min-h-44 overflow-hidden bg-gradient-to-br from-accent-pink via-white to-primary/10 p-4">
      <div class="absolute inset-0 opacity-70" :class="categoryWash"></div>
      <div class="relative flex h-full min-h-36 flex-col justify-between">
        <div class="flex items-start justify-between gap-3">
          <span class="badge bg-white/80">{{ displayType }}</span>
          <div class="flex items-center gap-2">
            <button
              class="grid h-8 w-8 place-items-center rounded-full bg-white/85 text-primary-dark shadow-sm transition hover:bg-accent-pink"
              @click.stop="$emit('toggle-save', product)"
              :aria-label="t('product.saveAria')"
            >
              <Heart class="h-4 w-4" :class="{ 'fill-primary text-primary': isSaved }" />
            </button>
            <span class="rounded-full bg-white/85 px-3 py-1 text-xs font-bold text-primary-dark shadow-sm">
              {{ product.matchScore }}%
            </span>
          </div>
        </div>

        <div class="flex items-end justify-between gap-4">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.16em] text-primary/75">{{ product.brand }}</p>
            <div class="mt-2 text-5xl font-display font-bold text-primary/20">
              {{ product.brand?.[0] || "S" }}
            </div>
          </div>
          <span class="rounded-2xl bg-primary-dark px-3 py-2 text-xs font-bold text-white shadow-sm">
            #{{ product.rank }}
          </span>
        </div>
      </div>
    </div>

    <div class="flex flex-1 flex-col p-4">
      <div class="mb-3 flex items-start justify-between gap-3">
        <h3 class="text-base font-bold leading-snug text-gray-950 transition-colors group-hover:text-primary">
          {{ product.name }}
        </h3>
        <span class="grid h-9 w-9 shrink-0 place-items-center rounded-2xl bg-primary/10 text-primary transition-all group-hover:bg-primary group-hover:text-white">
          <ArrowRight class="h-4 w-4" />
        </span>
      </div>

      <div class="mb-4 flex flex-wrap gap-1.5">
        <span
          v-for="ing in visibleIngredients"
          :key="ing"
          class="rounded-full border border-gray-100 bg-gray-50 px-2.5 py-1 text-[10px] font-semibold text-gray-500"
        >
          {{ ing }}
        </span>
      </div>

      <div class="mt-auto space-y-2 rounded-2xl bg-primary/5 p-3">
        <p class="text-[10px] font-bold uppercase tracking-[0.14em] text-primary/70">{{ t('product.whySuitable') }}</p>
        <ul class="space-y-1.5">
          <li
            v-for="point in visibleReasons"
            :key="point"
            class="line-clamp-1 text-xs font-semibold leading-5 text-primary-dark/85"
          >
            {{ point }}
          </li>
        </ul>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { ArrowRight, Heart } from "lucide-vue-next";
import { useLocaleStore } from "../stores/useLocaleStore";
import { displayCategory } from "../utils/analysisMapping";

const { t } = useI18n();
const locale = useLocaleStore();

const props = defineProps({
  product: Object,
  isSaved: Boolean,
});

const visibleIngredients = computed(() => (props.product?.ingredients || []).slice(0, 4));
const displayType = computed(() => displayCategory(props.product?.type || props.product?.displayType, locale.locale));
const visibleReasons = computed(() => {
  const points = props.product?.summaryPoints || props.product?.explanationFactors?.summary_points || [];
  if (points.length > 0) return points.slice(0, 2);
  return [props.product?.whyRecommended || t("product.fallbackWhy")];
});

const categoryWash = computed(() => {
  const type = props.product?.type || "";
  if (type.includes("sunscreen")) return "bg-[radial-gradient(circle_at_75%_18%,rgba(245,158,11,0.20),transparent_12rem)]";
  if (type.includes("cleanser")) return "bg-[radial-gradient(circle_at_75%_18%,rgba(59,130,246,0.16),transparent_12rem)]";
  if (type.includes("mask")) return "bg-[radial-gradient(circle_at_75%_18%,rgba(255,222,222,0.92),transparent_12rem)]";
  return "bg-[radial-gradient(circle_at_75%_18%,rgba(74,103,65,0.16),transparent_12rem)]";
});
</script>
