// components/CountrySelect.tsx
// import { Select } from "@/components/ui/select";

import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"

interface Props {
  countries: string[];
  selected: string;
  onChange: (value: string) => void;
  label: string;
}

const CountrySelect: React.FC<Props> = ({ countries, selected, onChange, label }) => (
        <Select onValueChange={onChange} defaultValue={selected}>
        <SelectTrigger className="w-[180px]">
            <SelectValue placeholder={label} />
        </SelectTrigger>
        <SelectContent>
            <SelectGroup>
            <SelectLabel>Fruits</SelectLabel>
            {countries.map((country, idx) => (
                <SelectItem key={idx} value={country}>
                    {country}
                </SelectItem>
            ))}
            </SelectGroup>
        </SelectContent>
        </Select>
);

export default CountrySelect;
