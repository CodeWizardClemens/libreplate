import SearchBar, { type SortOption } from "@/components/ui/SearchBar";

export type FoodSortMethod = "name" | "brand";

const SORT_OPTIONS: SortOption<FoodSortMethod>[] = [
  { value: "name", label: "Name" },
  { value: "brand", label: "Brand" },
];

interface Props {
  search: string;
  onSearchChange: (value: string) => void;

  showFavorites: boolean;
  onToggleFavorites: () => void;

  sortMethod: FoodSortMethod;
  onSortChange: (value: FoodSortMethod) => void;
}

export default function FoodSearchBar({
  search,
  onSearchChange,
  showFavorites,
  onToggleFavorites,
  sortMethod,
  onSortChange,
}: Props) {
  return (
    <SearchBar
      search={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Search foods..."
      showFavorites={showFavorites}
      onToggleFavorites={onToggleFavorites}
      sortMethod={sortMethod}
      onSortChange={onSortChange}
      sortOptions={SORT_OPTIONS}
      selectedTags={[]}
      onTagsChange={() => {}}
    />
  );
}